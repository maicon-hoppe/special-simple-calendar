from zoneinfo import ZoneInfo

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.views.decorators.http import require_GET

from google_user_auth.mods.auth import CalendarModelBackend
from homepage.models import CalendarEvent


@require_GET
def context_menu(request: HttpRequest) -> HttpResponse:
    """View for the menu on the top right of the page"""
    if request.htmx:
        authorization_url = CalendarModelBackend.authorize()

        return render(
            request, "html_assets/context-menu.html", {"auth_url": authorization_url}
        )
    else:
        return HttpResponseNotFound(404)


@require_GET
@login_required
def event_dialog(request: HttpRequest) -> HttpResponse:
    """View for the calendar event creation dialog"""
    if request.htmx:
        return render(request, "html_assets/event-dialog.html")
    else:
        return HttpResponseNotFound(404)


@require_GET
@login_required
def event_tiles(request: HttpRequest, year: int, month: int, day: int) -> HttpResponse:
    """View for loading calendar event tiles"""
    if request.htmx:
        all_day_events = CalendarEvent.objects.filter(
            Q(username__exact=request.user)
            & Q(start_point__year__lte=year)
            & Q(end_point__year__gte=year)
            & Q(start_point__month__lte=month)
            & Q(end_point__month__gte=month)
            & Q(start_point__day__lte=day)
            & Q(end_point__day__gte=day)
        )

        calendar_events = []
        for event in all_day_events:
            event.start_point = event.start_point.astimezone(ZoneInfo(event.timezone))
            event.end_point = event.end_point.astimezone(ZoneInfo(event.timezone))

            calendar_events.append(event)

        return render(
            request,
            "html_assets/event-tiles.html",
            {"calendar_events": calendar_events},
        )
    else:
        return HttpResponseNotFound(404)
