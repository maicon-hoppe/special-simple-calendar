from datetime import date
from typing import Any

from django.utils import dates
from django.views.generic import TemplateView
from django.views.generic.dates import MonthMixin


class HomepageView(MonthMixin, TemplateView):
    template_name = "homepage/index.html"
    month = "Julho"
    month_format = "%B"
