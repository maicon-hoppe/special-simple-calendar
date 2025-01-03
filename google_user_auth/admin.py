from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from homepage.models import CalendarEvent

from .models import CalendarUser


class CalendarEventAdmin(admin.TabularInline):
    model = CalendarEvent
    extra = 1


class CalendarUserAdmin(admin.ModelAdmin):

    fieldsets = [
        ("Usuário", {"fields": ["profile_picture", "first_name"]}),
        (None, {"fields": ["full_name"]}),
    ]

    inlines = [CalendarEventAdmin]


admin.site.register(CalendarUser, CalendarUserAdmin)
