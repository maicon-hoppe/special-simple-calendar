from datetime import date, timedelta
from typing import Any, Literal, Self

from django.views.generic import TemplateView
from django.views.generic.dates import MonthMixin, YearMixin


def get_month_list(
    month: int, year: int = date.today().year
) -> list[date] | Literal[-1]:
    """
    Returns a list with dates for the days of the month plus the
    beggining of the first week (Sunday) and the end of the last one (Saturday).
    Returns -1 if the month is invalid.
    """

    if 10 <= month <= 12:
        date_string = f"{year}-{month}-01"
    elif 1 <= month <= 9:
        date_string = f"{year}-0{month}-01"
    else:
        return -1

    this_month_first = date.fromisoformat(date_string)
    if this_month_first.weekday() == 6:
        first_monday = this_month_first
    else:
        first_monday = this_month_first - timedelta(days=this_month_first.isoweekday())

    return [first_monday + timedelta(days=c) for c in range(0, 42)]


class HomepageView(MonthMixin, TemplateView):
    template_name = "homepage/index.html"
    month_format = "%m"

    def get_context_data(self: Self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        context["date_list"] = get_month_list(date.today().month)
        context["today"] = {
            "year": date.today().year,
            "month": date.today().month,
            "day": date.today().day,
        }
        context["next"] = {
            "month": date.today().month + 1 if date.today().month < 12 else 1,
            "year": date.today().year + 1,
        }
        context["previous"] = {
            "month": date.today().month - 1 if date.today().month > 1 else 12,
            "year": date.today().year - 1,
        }

        return context


class MonthPageView(YearMixin, HomepageView):

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        context["date_list"] = get_month_list(self.get_month(), self.get_year())
        context["next"] = {
            "month": int(self.get_month()) + 1 if self.get_month() < 12 else 1,
            "year": self.get_year() + 1,
        }
        context["previous"] = {
            "month": self.get_month() - 1 if self.get_month() > 1 else 12,
            "year": self.get_year() - 1,
        }

        return context
