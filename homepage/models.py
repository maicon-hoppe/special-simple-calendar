from django.db import models
from django.utils.translation import gettext as _

from google_user_auth.models import CalendarUser


class EventColor(models.Model):
    color_id = models.IntegerField(_("ID da cor"), primary_key=True)

    foreground = models.CharField(_("Cor do texto"), max_length=9, blank=False)
    background = models.CharField(_("Cor de fundo"), max_length=9, blank=False)

    def __str__(self):
        return self.background


class CalendarEvent(models.Model):
    title = models.CharField(
        _("Título"), max_length=100, blank=False, null=True
    )  # summary
    description = models.TextField(_("Descrição"), blank=True, null=True)  # description

    start_point = models.DateTimeField(
        _("Início do evento (UTC)"), blank=False
    )  # start (UTC)
    end_point = models.DateTimeField(_("Fim do evento (UTC)"), blank=False)  # end (UTC)
    timezone = models.CharField(
        _("Fuso horário do evento"), max_length=100, blank=False, default='UTC'
    )  # start.timeZnoe

    event_color = models.ForeignKey(
        EventColor,
        verbose_name=_("Cor do evento"),
        blank=False,
        default=0,
        on_delete=models.SET_DEFAULT,
    )  # colorId

    username = models.ForeignKey(
        CalendarUser, verbose_name=_("Usuário"), default="", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title
