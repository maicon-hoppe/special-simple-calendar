from datetime import date, timedelta
from typing import Any, Literal, Self

from django.views.generic import TemplateView
from django.views.generic.dates import MonthMixin


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
    first_monday = this_month_first - timedelta(days=this_month_first.isoweekday())

    return [first_monday + timedelta(days=c) for c in range(0, 42)]


class HomepageView(MonthMixin, TemplateView):
    template_name = "homepage/index.html"
    month = "Julho"
    month_format = "%B"

    def get_context_data(self: Self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["date_list"] = get_month_list(date.today().month)
        return context
