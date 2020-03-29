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
from runduck.jobinfo import merge_projects

class JobInfoTestCase(unittest.TestCase):
    """Tests for  module"""
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        app.config.from_pyfile("../app.cfg")

    def test_read_all_data(self):
        data = read_environment(live_data_source=DataSource.FILE_SYSTEM)
        assert data

    def test_read_all_environments(self):
        data = read_all_environments(live_data_source=DataSource.API)
        env = next(iter(app.config["ENV"]))
        assert data[env]

    def test_combine_data(self):
        data = combine_data(live_data_source=DataSource.API)

    def test_merge_projects(self):
        projects1 = [
            {"description": "Administrative jobs", "name": "Admin", "url": "http://qa-url/Admin"},
            {"description": "Integrations to apps like slack and dynamo", "name": "App-Integrations", "url": "http://qa-url//App-Integrations"}
        ]
        projects2 = [
            {"description": "", "name": "App-Integrations", "url": "http://prod-url/App-Integrations"},
            {"description": "", "name": "BusinessSystems",  "url": "http://prod-url/BusinessSystems"}
        ]
        env1 = "qa"
        env2 = "prod"

        merged = merge_projects(projects1, projects2, env1, env2)
        assert set(merged.columns.tolist()) == {
            'project_name', 'project_description_qa', 'project_url_prod',
            'project_description_prod', 'project_url_qa'
        }
        assert merged.shape[0] == 3


