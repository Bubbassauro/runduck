"""Test the JobInfo class
python -m pytest -v -s
"""
import unittest
import pytest
from runduck import app
from runduck.datainteraction import DataSource
from runduck.jobinfo import read_environment
from runduck.jobinfo import read_all_environments
from runduck.jobinfo import combine_data

class JobInfoTestCase(unittest.TestCase):
    """Tests for  module"""
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        app.config.from_pyfile("../app.cfg")

    def test_read_all_data(self):
        data = read_environment(live_data_source=DataSource.FILE_SYSTEM)
        assert data

    def test_read_environment(self):
        env = "test"
        data = read_environment(live_data_source=DataSource.API, force_refresh=False, env=env)
        assert data

    def test_read_all_environments(self):
        data = read_all_environments(live_data_source=DataSource.API, force_refresh=False)
        env = next(iter(app.config["ENV"]))
        assert data[env]

    def test_combine_data(self):
        data = combine_data()

