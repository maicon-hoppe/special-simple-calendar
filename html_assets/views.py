from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.views.decorators.http import require_GET


@require_GET
def context_menu(request: HttpRequest) -> HttpResponse:
    if request.htmx:
        return render(request, "html_assets/context-menu.html")
    else:
        return HttpResponseNotFound(404)
