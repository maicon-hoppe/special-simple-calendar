from django.contrib import admin

from .models import CalendarEvent, EventColor


class CalendarEventsInline(admin.TabularInline):
    model = CalendarEvent
    extra = 1


class EventColorAdmin(admin.ModelAdmin):
    fields = ["color_id", "background"]
    list_display = ["color_id", "background"]

    inlines = [CalendarEventsInline]


class CalendarEventAdmin(admin.ModelAdmin):
    list_display = ["title", "description", "start_point", "end_point", "timezone"]
    list_filter = ["title", "start_point", "end_point", "timezone"]
    search_fields = ["title", "description"]


admin.site.register(CalendarEvent, CalendarEventAdmin)
admin.site.register(EventColor, EventColorAdmin)
