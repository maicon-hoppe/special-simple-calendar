from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as _logout
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect


def logout(request: HttpRequest) -> None:
    _logout(request)


def google_auth_response(request: HttpRequest) -> HttpResponse:
    try:
        user = authenticate(request)
    except PermissionDenied:
        return HttpResponse("<h1>Unauthorized</h1><hr>", status=401)
    else:
        if user:
            login(request, user)
            return redirect("homepage:homepage")
        else:
            return HttpResponse(f"Could not authenticate user: {user}", status=401)


def logout_view(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        request.user.delete()

    logout(request)
    return redirect("homepage:homepage")
