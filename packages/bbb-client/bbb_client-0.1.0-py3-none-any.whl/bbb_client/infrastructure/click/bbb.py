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

from typing import List

import click

from bbb_client.domain.meeting_management.model import (
    Bbb,
    BbbException,
    MeetingDoesNotExist,
)
from bbb_client.interfaces import from_terminal as controllers
from bbb_client.interfaces import to_terminal as presenters
from bbb_client.use_cases import search_meetings


def stdout(text: str) -> None:
    click.echo(text)


def stderr(text: str) -> None:
    click.echo(text, err=True)


@click.group()
@click.pass_context
def cli(ctx: click.Context) -> None:
    if not ctx.obj:
        ctx.obj = {}


@cli.group()
@click.pass_context
def meetings(ctx: click.Context) -> None:
    pass


@meetings.command()
@click.pass_context
def list(ctx: click.Context) -> None:
    """List all meetings."""

    bbb: Bbb = ctx.obj["bbb"]

    presenter = presenters.ListMeetings(stdout, stderr)
    interactor = search_meetings.Interactor(bbb, presenter)
    controller = controllers.ListMeetings()
    controller.call(interactor)
    ctx.exit(presenter.exit_code())


@meetings.command()
@click.argument("filters", nargs=-1, required=True)
@click.pass_context
def search(ctx: click.Context, filters: List[str]) -> None:
    """Only return meetings matching some criteria.

    Filters are a name/value paire, for instance `voiceBridge=12345`.
    """

    bbb: Bbb = ctx.obj["bbb"]

    separator = "="
    presenter = presenters.SearchMeetings(stdout, stderr, separator)
    interactor = search_meetings.Interactor(bbb, presenter)
    controller = controllers.SearchMeetings(filters, separator)
    controller.call(interactor)
    ctx.exit(presenter.exit_code())


@meetings.command()
@click.argument("id")
@click.argument("name", required=False, default="")
@click.option("--moderator-password", "-M", default="")
@click.option("--attendee-password", "-A", default="")
@click.option("--max-participants", "-P", default=0)
@click.pass_context
def create(
    ctx: click.Context,
    id: str,
    name: str,
    moderator_password: str,
    attendee_password: str,
    max_participants: int,
) -> None:
    """Create a new meeting."""

    if not name:
        name = id

    bbb: Bbb = ctx.obj["bbb"]
    status = bbb.create_meeting(
        id,
        name=name,
        moderator_password=moderator_password,
        attendee_password=attendee_password,
        max_participants=max_participants,
    )

    if status:
        click.echo("[OK] Meeting successfully created!")
    else:
        click.echo("[ER] Meeting could not be created!")


@meetings.command()
@click.argument("meeting")
@click.argument("user")
@click.argument("password", default="")
@click.option("--moderator", "-m", is_flag=True, default=False)
@click.pass_context
def join(
    ctx: click.Context, meeting: str, user: str, password: str, moderator: bool
) -> None:
    """Create an URL to be used to join an existing meeting."""

    bbb: Bbb = ctx.obj["bbb"]
    try:
        url = bbb.generate_join_url(meeting, user, password, moderator=moderator)
        click.echo(url)
    except BbbException as exc:
        click.echo(f"[ER] {exc}")


@meetings.command()
@click.argument("id")
@click.pass_context
def show(ctx: click.Context, id: str) -> None:
    """Show information for a given meeting."""

    bbb: Bbb = ctx.obj["bbb"]
    try:
        info = bbb.meeting_info(id)
        click.echo(f'Name: "{info.meetingName}"')
        click.echo(f"ID: {info.meetingID}")
        click.echo(f"Participants: {info.participantCount}")
        click.echo(f"Audio-conf. PIN: {info.voiceBridge}")
    except MeetingDoesNotExist:
        click.echo(f"[ER] Meeting '{id}' does not exist!")


@meetings.command()
@click.argument("id")
@click.pass_context
def end(ctx: click.Context, id: str) -> None:
    """End a given meeting."""

    bbb: Bbb = ctx.obj["bbb"]

    try:
        status = bbb.end_meeting(id)
    except MeetingDoesNotExist:
        click.echo(f"[ER] Meeting '{id}' does not exist!")
        return

    if status:
        click.echo("[OK] Meeting successfully ended!")
    else:
        click.echo("[ER] Meeting could not be ended!")


@meetings.command()
@click.pass_context
def stats(ctx: click.Context) -> None:
    """Display statistics about all meetings."""

    bbb: Bbb = ctx.obj["bbb"]
    stats = bbb.stats()

    if stats:
        for k, v in stats.items():
            click.echo(f'{v} participant(s) in "{k}"')
    else:
        click.echo("There are no meetings at the moment.")
