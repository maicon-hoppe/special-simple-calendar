from datetime import UTC
from typing import Any, Literal, Self
from zoneinfo import ZoneInfo

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.utils.dates import WEEKDAYS_ABBR
from django.utils.timezone import datetime, timedelta
from django.views.decorators.http import require_GET
from django.views.generic import TemplateView
from django.views.generic.dates import MonthMixin, YearMixin

from google_user_auth.mods.auth import CalendarModelBackend
from google_user_auth.mods.orm.external import CalendarUserData
from homepage.models import CalendarEvent, EventColor


def get_month_list(
    month: int, year: int = datetime.today().year
) -> list[datetime] | Literal[-1]:
    """
    Returns a list with dates for the days of the month plus the
    beggining of the first week (Sunday) and the end of the last one (Saturday).
    Returns -1 if the month is invalid.
    """

    if 10 <= month <= 12:
        date_string = f"{year}-{month}-01"
    elif 1 <= month <= 9:
        date_string = f"{year}-0{month}-01"
    else:
        return -1

    this_month_first = datetime.fromisoformat(date_string)
    if this_month_first.weekday() == 6:
        first_monday = this_month_first
    else:
        first_monday = this_month_first - timedelta(days=this_month_first.isoweekday())

    return [first_monday + timedelta(days=c) for c in range(0, 42)]


class HomepageView(MonthMixin, TemplateView):
    month_format = "%m"

    def get_template_names(self):
        if self.request.user.is_authenticated:
            return ["homepage/autheticated_index.html"]
        else:
            return ["homepage/index.html"]

    def get_context_data(self: Self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            month_events = CalendarEvent.objects.filter(
                Q(username__exact=self.request.user)
                & Q(start_point__month__gte=datetime.now(ZoneInfo("UTC")).month)
                & Q(end_point__month__lte=datetime.now(ZoneInfo("UTC")).month)
            )
            context["calendar_events"] = []
            for event in month_events:
                event.start_point = event.start_point.astimezone(
                    ZoneInfo(event.timezone)
                )
                event.end_point = event.end_point.astimezone(ZoneInfo(event.timezone))

                context["calendar_events"].append(event)

        context["date_list"] = get_month_list(datetime.today().month)
        context["today"] = {
            "year": datetime.today().year,
            "month": datetime.today().month,
            "day": datetime.today().day,
        }
        context["next"] = {
            "month": datetime.today().month + 1 if datetime.today().month < 12 else 1,
            "year": datetime.today().year + 1,
        }
        context["previous"] = {
            "month": datetime.today().month - 1 if datetime.today().month > 1 else 12,
            "year": datetime.today().year - 1,
        }
        context["week_days"] = WEEKDAYS_ABBR

        return context


class MonthPageView(YearMixin, HomepageView):

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            month_events = CalendarEvent.objects.filter(
                Q(username__exact=self.request.user)
                & Q(start_point__month__gte=datetime.now(ZoneInfo("UTC")).month)
                & Q(end_point__month__lte=datetime.now(ZoneInfo("UTC")).month)
            )
            context["calendar_events"] = []
            for event in month_events:
                event.start_point = event.start_point.astimezone(
                    ZoneInfo(event.timezone)
                )
                event.end_point = event.end_point.astimezone(ZoneInfo(event.timezone))

                context["calendar_events"].append(event)

        context["date_list"] = get_month_list(self.get_month(), self.get_year())
        context["next"] = {
            "month": int(self.get_month()) + 1 if self.get_month() < 12 else 1,
            "year": self.get_year() + 1,
        }
        context["previous"] = {
            "month": self.get_month() - 1 if self.get_month() > 1 else 12,
            "year": self.get_year() - 1,
        }

        return context


@login_required
@require_GET
def login_redirect_view(request: HttpRequest) -> HttpResponse:
    creds = CalendarModelBackend.build_user_credentials(request.user)
    user_data = CalendarUserData(creds)

    CalendarEvent.objects.filter(username__exact=request.user).delete()
    EventColor.objects.all().delete()

    all_event_colors = user_data.get_event_colors().items()
    EventColor.objects.bulk_create(
        [
            EventColor(
                color_id=key,
                foreground=value["foreground"],
                background=value["background"],
            )
            for key, value in all_event_colors
        ]
    )
    default_color = user_data.get_calendar_color()
    EventColor(0, foreground="#1d1d1d", background=default_color).save()

    all_events = user_data.get_year_events(datetime.today().year)
    CalendarEvent.objects.bulk_create(
        [
            CalendarEvent(
                title=event.get("summary", None),
                description=event.get("description", None),
                start_point=datetime.fromisoformat(
                    event["start"].get("dateTime", event["start"].get("date"))
                ).astimezone(UTC),
                end_point=(
                    datetime.fromisoformat(event["end"].get("dateTime")).astimezone(UTC)
                    if event["end"].get("dateTime")
                    else datetime.fromisoformat(event["end"].get("date")).astimezone(
                        UTC
                    )
                    - timedelta(minutes=1)
                ),
                timezone=(event["start"].get("timeZone", request.user.local_timezone)),
                event_color=EventColor.objects.get(pk=event.get("colorId", 0)),
                username=request.user,
            )
            for event in all_events
        ]
    )

    return redirect("homepage:homepage", permanent=True)
