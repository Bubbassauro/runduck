"""Test the JobInfo class
python -m pytest -v -s
"""
import unittest
import pytest
from runduck import app
from runduck.datainteraction import DataSource
from runduck.jobinfo import read_all_data


class JobInfoTestCase(unittest.TestCase):
    """Tests for  module"""

    def test_read_all_data(self):
        data = read_all_data(live_data_source=DataSource.FILE_SYSTEM)
        assert data
