from typing import Annotated, Final, Never, Optional, TypeAlias

from django.contrib.auth.backends import ModelBackend
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from google_auth_oauthlib.flow import Flow

from google_user_auth.models import CalendarUser


class CalendarModelBackend(ModelBackend):

    GoogleApiScopes: TypeAlias = list[Annotated[str, "API endpoint"]]
    __SCOPES: Final[GoogleApiScopes] = [
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/calendar.readonly",
        "https://www.googleapis.com/auth/calendar.calendarlist.readonly",
        "https://www.googleapis.com/auth/calendar.calendars.readonly",
        "https://www.googleapis.com/auth/calendar.calendars.readonly",
        "https://www.googleapis.com/auth/calendar.events.freebusy",
        "https://www.googleapis.com/auth/calendar.events.owned",
        "https://www.googleapis.com/auth/calendar.events.public.readonly",
    ]
    __STATE: Optional[str] = None
    __FLOW: Optional[Flow] = None

    @classmethod
    def authorize(cls) -> Annotated[str, "Authorization URL"]:
        from pathlib import Path

        flow = Flow.from_client_secrets_file(
            f"{Path(__file__).parent.parent.parent.resolve()}/static/json/credentials.json",
            scopes=cls.__SCOPES,
        )
        flow.redirect_uri = "http://localhost:8000/accounts/"
        cls.__FLOW = flow

        authorization_url, state = flow.authorization_url(
            access_type="offline", include_granted_scopes="true", prompt="consent"
        )

        cls.__STATE = state
        return authorization_url

    def authenticate(
        self,
        request: HttpRequest,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ) -> Optional[CalendarUser] | Never:
        """Returns a user given the credentials as arguments or in request.
        If credentials are not valid raises PermissionDenied.
        if user is inactive returns None.
        """
        from django.core.exceptions import PermissionDenied
        from googleapiclient.discovery import build

        if username and password:
            user = get_object_or_404(CalendarUser, google_id__exact=username)

            if user.check_password(password) and self.user_can_authenticate(user):
                return user
            else:
                raise PermissionDenied("Unauthorized")
        elif self.__STATE == request.GET.get("state") and self.__FLOW:
            user_info = {}

            flow = self.__FLOW
            flow.fetch_token(code=request.GET.get("code"))
            user_info["access_token"] = flow.credentials.token
            user_info["refresh_token"] = flow.credentials.refresh_token
            user_info["expiry"] = flow.credentials.expiry

            user_service = build("oauth2", "v2", credentials=flow.credentials)
            result = user_service.userinfo().get().execute()
            user_info["google_id"] = result["id"]
            user_info["first_name"] = result["given_name"]
            user_info["full_name"] = result["name"]
            user_info["profile_picture"] = result["picture"]

            new_user = CalendarUser(**user_info)

            new_user.save()
            return new_user if self.user_can_authenticate(new_user) else None
        else:
            raise PermissionDenied("Unauthorized")

    @staticmethod
    def get_user(user_id: str) -> Optional[CalendarUser]:
        try:
            user = CalendarUser.objects.get(pk=user_id)
        except CalendarUser.DoesNotExist:
            return None
        else:
            return user
