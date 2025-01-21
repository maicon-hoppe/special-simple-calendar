from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseNotFound
from django.views.generic import DetailView, ListView, TemplateView

from google_user_auth.mods.auth import CalendarModelBackend
from homepage.models import CalendarEvent


class ContextMenuView(TemplateView):
    """View for the menu on the top right of the page"""

    template_name = "html_assets/context-menu.html"

    def dispatch(self, request, *args, **kwargs):
        if request.method != "GET":
            return HttpResponseNotAllowed(request.method)

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["auth_url"] = CalendarModelBackend.authorize()
        return context


class ShowEventDialogView(DetailView):
    """View for displaying a calendar event"""

    model = CalendarEvent
    template_name = "html_assets/show-event-dialog.html"

    def dispatch(self, request, *args, **kwargs):
        if request.method != "GET":
            return HttpResponseNotAllowed(request.method)

        return super().dispatch(request, *args, **kwargs)


class EventTilesView(LoginRequiredMixin, ListView):
    """View for loading calendar event tiles"""

    model = CalendarEvent
    template_name = "html_assets/event-tiles.html"

    def get_queryset(self) -> list[CalendarEvent]:
        return CalendarEvent.objects.filter(
            Q(username__exact=self.request.user)
            & Q(start_point__year__lte=self.kwargs["year"])
            & Q(end_point__year__gte=self.kwargs["year"])
            & Q(start_point__month__lte=self.kwargs["month"])
            & Q(end_point__month__gte=self.kwargs["month"])
            & Q(start_point__day__lte=self.kwargs["day"])
            & Q(end_point__day__gte=self.kwargs["day"])
        )

    def dispatch(self, request, *args, **kwargs):
        if request.method != "GET":
            return HttpResponseNotAllowed(request.method)

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs) -> HttpResponse:
        if request.htmx:
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponseNotFound(404)


class EventListView(EventTilesView):
    template_name = "html_assets/event-list.html"
