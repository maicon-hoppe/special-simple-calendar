from django.urls import path

from . import views

app_name = "html_assets"
urlpatterns = [
    path("context_menu/", views.context_menu, name="context_menu"),
    path("event_dialog/", views.event_dialog, name="event_dialog"),
    path("event_tiles/<int:year>/<int:month>/<int:day>/", views.event_tiles, name="event_tiles"),
]
