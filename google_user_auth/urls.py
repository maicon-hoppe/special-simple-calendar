from django.urls import path

from . import views

app_name = "google_user_auth"
urlpatterns = [
    path("", views.google_auth_response, name="api_redirect"),
    path("logout/", views.logout_view, name="logout_view"),
]
