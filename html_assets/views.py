from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.views.decorators.http import require_GET

from google_user_auth.mods.auth import CalendarModelBackend


@require_GET
def context_menu(request: HttpRequest) -> HttpResponse:
    if request.htmx:
        authorization_url = CalendarModelBackend.authorize()

        return render(
            request, "html_assets/context-menu.html", {"auth_url": authorization_url}
        )
    else:
        return HttpResponseNotFound(404)
