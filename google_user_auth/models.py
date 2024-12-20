from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext as _

from .mods.orm import CalendarUserManager


class CalendarUser(AbstractBaseUser, PermissionsMixin):
    """
    Definition of Google calendar Users.
    """

    google_id = models.CharField(
        _("ID do usuário"), max_length=100, editable=False, unique=True
    )

    first_name = models.CharField(
        _("Nome de usuário"), default="user", blank=False, max_length=50
    )  # given_name

    full_name = models.CharField(
        _("Nome Completo"), default="user", blank=False, max_length=100
    )  # name

    profile_picture = models.URLField(_("Imagem de perfil"), default="png", blank=False)

    access_token = models.CharField(
        _("Token de acesso"),
        max_length=255,
        editable=False,
    )

    refresh_token = models.CharField(
        _("Token de substituição"), max_length=255, editable=False
    )

    expiry = models.DateTimeField(_("Expiração do token"), blank=False, max_length=27)

    is_staff = models.BooleanField(_("Is staff"), default=False)
    is_superuser = models.BooleanField(_("Is superuser"), default=False)

    objects = CalendarUserManager()

    USERNAME_FIELD = "google_id"
    REQUIRED_FIELDS = ["access_token", "refresh_token", "expiry"]

    def __str__(self):
        return self.first_name

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.first_name
