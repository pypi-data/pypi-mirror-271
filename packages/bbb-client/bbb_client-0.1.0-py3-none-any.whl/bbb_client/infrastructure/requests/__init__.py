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

import hashlib
from urllib.parse import urlencode

import requests

from bbb_client.domain.meeting_management.model import BbbApi, BbbException


class BadResponseFromServer(BbbException):
    def __init__(self, url: str, response: requests.Response):
        super().__init__(
            f"Bad response from BBB API: {response.status_code}. "
            f"Please check URL: <{url}>."
        )
        self.url = url
        self.response = response


class AccessForbidden(BbbException):
    def __init__(self, url: str):
        super().__init__("Access forbidden! Make sure your secret is correct.")
        self.url = url


class RequestsBbbApi(BbbApi):
    def __init__(self, an_url: str, a_secret: str) -> None:
        self.__url = an_url
        self.__secret = a_secret

    def get_meetings(self) -> str:
        return self.__get_xml(self.__build_url("getMeetings"))

    def __build_url(self, action: str, query: str = "") -> str:
        checksum = self.__compute_checksum(action, query, self.__secret)
        return f"{self.__url}/{action}?{query}&checksum={checksum}"

    def __get_xml(self, url: str) -> str:
        response = requests.get(url)
        if self.__is_success(response) and self.__is_xml(response):
            return response.text
        self.__handle_bad_response(url, response)
        return ""

    def __is_success(self, response: requests.Response) -> bool:
        return 200 <= response.status_code < 300

    def __is_xml(self, response: requests.Response) -> bool:
        return response.headers.get("content-type", "").startswith("text/xml")

    def __handle_bad_response(self, url: str, response: requests.Response) -> None:
        if response.status_code == 401:
            raise AccessForbidden(url)
        raise BadResponseFromServer(url, response)

    def __compute_checksum(self, action: str, query: str, secret: str) -> str:
        return hashlib.sha1(str.encode(f"{action}{query}{secret}")).hexdigest()

    def create(
        self,
        an_id: str,
        name: str = "",
        moderator_password: str = "",
        attendee_password: str = "",
        max_participants: int = 0,
    ) -> str:
        query = {"meetingID": an_id}
        if name:
            query["name"] = name
        if moderator_password:
            query["moderatorPW"] = moderator_password
        if attendee_password:
            query["attendeePW"] = attendee_password
        if max_participants:
            query["maxParticipants"] = str(max_participants)

        return self.__get_xml(self.__build_url("create", urlencode(query)))

    def generate_join_url(self, an_id: str, a_username: str, a_password: str) -> str:
        query = {"fullName": a_username, "meetingID": an_id, "password": a_password}
        return self.__build_url("join", urlencode(query))

    def get_meeting_info(self, an_id: str) -> str:
        query = {"meetingID": an_id}
        return self.__get_xml(self.__build_url("getMeetingInfo", urlencode(query)))

    def end(self, an_id: str, a_password: str) -> str:
        query = {"meetingID": an_id, "password": a_password}
        return self.__get_xml(self.__build_url("end", urlencode(query)))
