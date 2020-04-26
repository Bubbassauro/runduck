"""Test helper functions
python -m pytest runduck/tests/test_utils.py -v -s --disable-warnings -k test_get_elapsed_time
"""
import unittest
import pytest
from runduck.utils import get_elapsed_time
from runduck.utils import get_object_property
from runduck.utils import convert_hour_range


class UtilsTestCase(unittest.TestCase):
    """Tests for  module"""

    def test_get_elapsed_time(self):
        start_date = "2020-04-19T22:05:00Z"
        end_date = "2020-04-19T22:12:12Z"
        elapsed = get_elapsed_time(start_date, end_date)
        assert elapsed == "07m 12s"

    def test_get_elapsed_time_hours(self):
        start_date = "2020-04-19T22:05:00Z"
        end_date = "2020-04-19T23:12:12Z"
        elapsed = get_elapsed_time(start_date, end_date)
        assert elapsed == "1h 07m 12s"

    def test_get_object_property(self):
        obj = {
            "date-started": {"unixtime": 1587333900143, "date": "2020-04-19T22:05:00Z"}
        }
        assert get_object_property(obj, "date-started.date") == "2020-04-19T22:05:00Z"
        assert get_object_property(obj, "date-started.mising", "abc") == "abc"
        assert get_object_property(obj, "missing") is None

    def test_convert_hour_range(self):
        assert convert_hour_range("9-8") == "9-23,0-8"
        assert convert_hour_range("7-02/1") == "7-23/1,0-2/1"
