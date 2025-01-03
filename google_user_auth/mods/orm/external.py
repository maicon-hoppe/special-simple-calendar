from datetime import datetime, timedelta
from typing import Any
from zoneinfo import ZoneInfo

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


class CalendarUserData:
    """
    Represents the user's data from Google Calendar API
    """

    def __init__(self, user_credentials: Credentials) -> None:
        self._user_credentials = user_credentials

    def _get_service(self):
        service = None
        if not service:
            service = build("calendar", "v3", credentials=self._user_credentials)

        return service

    def get_year_events(self, year: int) -> list[dict[str, str | dict]]:
        """
        Returns a dictionary with all the events for a given year,
        in the users timezone, plus the beggining of the first
        week (Sunday) and the end of the last one (Saturday)
        """

        service = self._get_service()

        user_tz = ZoneInfo(self.get_user_timezone())
        first_sunday = (
            (datetime.fromisocalendar(year, 1, 1) - timedelta(days=1))
            .astimezone(user_tz)
            .isoformat()
        )
        last_day = datetime(year, 12, 31)
        if last_day.isoweekday() == 6:
            last_saturday = last_day.astimezone(user_tz).isoformat()
        elif last_day.isoweekday() < 6:
            difference_to_saturday = (last_day - timedelta(days=6)).isoweekday()
            last_saturday = (
                (last_day + timedelta(days=difference_to_saturday))
                .astimezone(user_tz)
                .isoformat()
            )
        elif last_day.isoweekday() == 7:
            last_saturday = (
                (last_day + timedelta(days=7)).astimezone(user_tz).isoformat()
            )

        calendar_events: dict = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=first_sunday,
                timeMax=last_saturday,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )

        return calendar_events["items"]

    def get_event_colors(self) -> dict[int, dict[str, str]]:
        """
        Returns a dictionary with all the colors for events
        """

        service = self._get_service()
        calendar_colors: dict = service.colors().get().execute()

        return calendar_colors["event"]

    def get_user_timezone(self) -> str:
        """Returns the user's timezone"""
        service = self._get_service()
        user_tz = service.settings().get(setting="timezone").execute()
        return user_tz["value"]

    def get_calendar_color(self) -> str:
        """Returns the user's primary calendar colorId"""
        service = self._get_service()
        calendar_list_entry = service.calendarList().get(calendarId="primary").execute()

        return calendar_list_entry["backgroundColor"]
