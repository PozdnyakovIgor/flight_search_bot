import unittest
from utils.check_date import check_date


class TestCheckDate(unittest.TestCase):
    def test_check_full_date(self):
        date = '2023-11-11'
        result = check_date(date)
        self.assertTrue(result)

    def test_check_short_date(self):
        date = "2023-11"
        result = check_date(date)
        self.assertTrue(result)

    def test_check_wrong_format_date(self):
        date = "20231111"
        result = check_date(date)
        self.assertFalse(result)

    def test_check_past_date(self):
        date = "2022-11-01"
        result = check_date(date)
        self.assertFalse(result)

    def test_check_wrong_month(self):
        date = "2023-20-11"
        result = check_date(date)
        self.assertFalse(result)

    def test_check_wrong_day(self):
        date = "2023-11-32"
        result = check_date(date)
        self.assertFalse(result)

    def test_check_retards(self):
        date = "aaaaa777"
        result = check_date(date)
        self.assertFalse(result)
