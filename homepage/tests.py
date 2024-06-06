from datetime import date, timedelta
from typing import Self

from django.test import SimpleTestCase

from homepage.views import get_month_list


class HomepageHelperFunctionsTests(SimpleTestCase):

    def test_get_month_list_valid_month(self: Self) -> None:
        """
        get_month_list() returns a list with dates for the days of the month plus the
        beggining of the first week (Sunday) and the end of the last one (Saturday)
        """

        january_list = get_month_list(1, 2024)
        self.assertEqual(
            january_list,
            [date(2023, 12, 31) + timedelta(days=c) for c in range(0, 42)],
            "Lists don't match.",
        )

    def test_get_month_list_invalid_month(self: Self) -> None:
        """
        get_month_list() returns -1 if the month is invalid
        """

        self.assertEqual(get_month_list(12000, 2024), -1, "Lists don't match.")
        self.assertEqual(get_month_list(13, 2024), -1, "Lists don't match.")
        self.assertEqual(get_month_list(0, 2024), -1, "Lists don't match.")
        self.assertEqual(get_month_list(-1, 2024), -1, "Lists don't match.")
