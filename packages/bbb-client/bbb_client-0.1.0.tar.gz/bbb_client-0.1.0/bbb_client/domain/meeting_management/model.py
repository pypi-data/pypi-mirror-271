# bbb-client --- Client library and CLI to interact with the BBB API
# Copyright © 2021, 2024 Easter-eggs
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Foobar.  If not, see <https://www.gnu.org/licenses/>.

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import untangle  # type: ignore


class BbbException(Exception):
    pass


class MeetingDoesNotExist(BbbException):
    pass


class ChecksumError(BbbException):
    def __init__(self) -> None:
        super().__init__("Checksum error! Please verify your shared secret.")


class UnixTimestamp(int):
    pass


@dataclass(frozen=True)
class MeetingInfo:
    """
    See <https://docs.bigbluebutton.org/dev/api.html#getmeetinginfo>
    """

    meetingName: str
    meetingID: str
    createTime: UnixTimestamp
    startTime: UnixTimestamp
    endTime: UnixTimestamp
    attendeePW: str
    moderatorPW: str
    duration: int
    participantCount: int
    maxUsers: int
    voiceBridge: str


@dataclass()
class MeetingFilters:
    voiceBridge: Optional[str] = ""


class BbbApi(ABC):
    @abstractmethod
    def get_meetings(self) -> str:
        pass

    @abstractmethod
    def create(
        self,
        an_id: str,
        name: str = "",
        moderator_password: str = "",
        attendee_password: str = "",
        max_participants: int = 0,
    ) -> str:
        pass

    @abstractmethod
    def generate_join_url(self, an_id: str, a_username: str, a_password: str) -> str:
        pass

    @abstractmethod
    def get_meeting_info(self, an_id: str) -> str:
        pass

    @abstractmethod
    def end(self, an_id: str, a_password: str) -> str:
        pass


class Bbb:
    def __init__(self, a_bbb_api: BbbApi) -> None:
        self.__api = a_bbb_api

    def meetings(self, filters: Optional[MeetingFilters] = None) -> List[MeetingInfo]:
        element = self.__xml_to_element(self.__api.get_meetings())

        if not hasattr(element.response.meetings, "meeting"):
            return []

        return self.__filter(
            [
                self.__element_to_meeting_info(e)
                for e in element.response.meetings.meeting
            ],
            filters,
        )

    def __xml_to_element(self, xml: str) -> Any:
        element = untangle.parse(xml)
        if self.__is_success(element):
            return element
        if element.response.messageKey.cdata == "notFound":
            raise MeetingDoesNotExist()
        if element.response.messageKey.cdata == "checksumError":
            raise ChecksumError()
        raise Exception(xml)

    def __is_success(self, element: untangle.Element) -> bool:
        return bool(element.response.returncode.cdata == "SUCCESS")

    def __element_to_meeting_info(self, element: Any) -> MeetingInfo:
        return MeetingInfo(
            meetingName=element.meetingName.cdata,
            meetingID=element.meetingID.cdata,
            createTime=element.createTime.cdata,
            startTime=element.startTime.cdata,
            endTime=element.endTime.cdata,
            attendeePW=element.attendeePW.cdata,
            moderatorPW=element.moderatorPW.cdata,
            duration=element.duration.cdata,
            participantCount=element.participantCount.cdata,
            maxUsers=element.maxUsers.cdata,
            voiceBridge=element.voiceBridge.cdata,
        )

    def create_meeting(
        self,
        a_meeting_id: str,
        name: str = "",
        moderator_password: str = "",
        attendee_password: str = "",
        max_participants: int = 0,
    ) -> bool:
        element = untangle.parse(
            self.__api.create(
                a_meeting_id,
                name=name,
                moderator_password=moderator_password,
                attendee_password=attendee_password,
                max_participants=max_participants,
            )
        )
        return self.__is_success(element)

    def generate_join_url(
        self,
        a_meeting_id: str,
        a_user_name: str,
        a_password: str = "",
        moderator: bool = False,
    ) -> str:
        if a_password:
            password = a_password
        else:
            info = self.meeting_info(a_meeting_id)

            if moderator:
                password = info.moderatorPW
            else:
                password = info.attendeePW

        if not password:
            raise BbbException(
                "Meeting does not yet exist, "
                "you MUST provide a password to include in the URL."
            )
        return self.__api.generate_join_url(a_meeting_id, a_user_name, password)

    def meeting_info(self, a_meeting_id: str) -> MeetingInfo:
        element = self.__xml_to_element(self.__api.get_meeting_info(a_meeting_id))
        return self.__element_to_meeting_info(element.response)

    def end_meeting(self, a_meeting_id: str) -> bool:
        info = self.meeting_info(a_meeting_id)
        element = untangle.parse(self.__api.end(a_meeting_id, info.moderatorPW))
        return self.__is_success(element)

    def stats(self) -> Dict[str, int]:
        return {m.meetingID: m.participantCount for m in self.meetings()}

    def __filter(
        self, meetings: List[MeetingInfo], filters: Optional[MeetingFilters]
    ) -> List[MeetingInfo]:
        if not filters:
            return meetings

        results = meetings
        if filters.voiceBridge:
            results = [m for m in results if filters.voiceBridge == m.voiceBridge]

        return results
