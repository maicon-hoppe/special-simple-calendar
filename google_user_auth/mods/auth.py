import json
from typing import Annotated, ClassVar, Final, Optional, TypeAlias

from django.contrib.auth.backends import ModelBackend
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow

from google_user_auth.models import CalendarUser
from special_simple_calendar.settings import BASE_DIR

from .orm.external import CalendarUserData


class CalendarModelBackend(ModelBackend):

    GoogleApiScopes: TypeAlias = list[Annotated[str, "API endpoint"]]
    __SCOPES: Final[GoogleApiScopes] = [
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/calendar.calendarlist.readonly",
        "https://www.googleapis.com/auth/calendar.calendars.readonly",
        "https://www.googleapis.com/auth/calendar.events.owned.readonly",
        "https://www.googleapis.com/auth/calendar.readonly",
        "https://www.googleapis.com/auth/calendar.events",
        "https://www.googleapis.com/auth/calendar.events.freebusy",
        "https://www.googleapis.com/auth/calendar.events.public.readonly",
        "https://www.googleapis.com/auth/calendar.events.owned",
    ]
    __STATE: ClassVar[Optional[str]] = None
    __FLOW: ClassVar[Optional[Flow]] = None

    @classmethod
    def authorize(cls) -> Annotated[str, "Authorization URL"]:
        flow = Flow.from_client_secrets_file(
            f"{BASE_DIR}/static/json/credentials.json",
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
    ) -> Optional[CalendarUser]:
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

            user_data = CalendarUserData(flow.credentials)
            user_info["local_timezone"] = user_data.get_user_timezone()

            if not CalendarUser.objects.filter(
                google_id__exact=user_info["google_id"]
            ).first():
                new_user = CalendarUser.objects.create(**user_info)
            else:
                new_user = CalendarUser.objects.get(
                    google_id__exact=user_info["google_id"]
                )

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

    @classmethod
    def get_scopes(cls) -> GoogleApiScopes:
        return cls.__SCOPES.copy()

    @classmethod
    def build_user_credentials(cls, user: CalendarUser) -> Credentials:
        credentials_file = f"{BASE_DIR}/static/json/credentials.json"
        with open(credentials_file, "r") as target:
            data = json.load(target)
            auth_token = {
                "access_token": user.access_token,
                "refresh_token": user.refresh_token,
                "client_id": data["web"]["client_id"],
                "client_secret": data["web"]["client_secret"],
            }

        creds = Credentials.from_authorized_user_info(auth_token, cls.get_scopes())

        if creds.expired:
            creds.refresh(Request())

        return creds
