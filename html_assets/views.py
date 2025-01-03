from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.views.decorators.http import require_GET

from google_user_auth.mods.auth import CalendarModelBackend


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
