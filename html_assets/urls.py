from django.urls import path

from . import views

app_name="html_assets"
urlpatterns = [path("context_menu/", views.context_menu, name="context_menu")]
