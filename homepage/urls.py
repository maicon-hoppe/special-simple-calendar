from django.urls import path

from . import views

app_name = "homepage"
urlpatterns = [
    path("", views.HomepageView.as_view(), name="homepage"),
    path("<int:year>/<int:month>/", views.MonthPageView.as_view(), name="month_page"),
    path("login_redirect/", views.login_redirect_view, name="login_redirect"),
]
