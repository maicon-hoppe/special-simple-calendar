from django.urls import path

from . import views

app_name = "html_assets"
urlpatterns = [
    path("context_menu/", views.ContextMenuView.as_view(), name="context_menu"),
    path("show_event_dialog/<int:pk>/", views.ShowEventDialogView.as_view(), name="show_event_dialog"),
    path("create_event_dialog/", views.create_event_dialog, name="create_event_dialog"),
    path("event_tiles/<int:year>/<int:month>/<int:day>/", views.EventTilesView.as_view(), name="event_tiles"),
]
