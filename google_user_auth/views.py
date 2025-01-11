from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect


def google_auth_response(request: HttpRequest) -> HttpResponse:
    try:
        user = authenticate(request)
    except PermissionDenied:
        return HttpResponse("<h1>Unauthorized</h1><hr>", status=401)
    else:
        if user:
            login(request, user)
            return redirect("homepage:homepage", permanent=True)
        else:
            return HttpResponse("<h1>Could not authenticate user</h1><hr>", status=401)


@login_required
def logout_view(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated and not request.user.is_superuser:
        request.user.delete()

    logout(request)
    return redirect("homepage:homepage")
