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
from runduck.jobinfo import append_info
from runduck.jobinfo import find_job
from runduck.jobinfo import get_job_details

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

    def test_append_project_info(self):
        job = {"id": "dbaa0ddb-596b-410d-9fa1-a96166724699", "name": "analyze"}
        project = {
            'description': 'Administrative jobs',
            'name': 'Admin',
            'url': 'http://devops.equinoxfitness.com/rundeck/api/24/project/Admin'
        }
        job_project = append_info(job=job, project=project, env="prod")
        assert "project_name" in job_project
        assert "project_description" in job_project
        assert "project_url" in job_project
        assert "id" in job_project
        assert "env" in job_project
        assert "euid" in job_project # unique id across all environments

    def test_find_job(self):
        jobs = [
            {'uuid': 'c7d3aea1-28af-4c14-9580-3792fe0e52f0', 'name': 'cache_rd',
                'id': 'prod.c7d3aea1-28af-4c14-9580-3792fe0e52f0',
                'project': 'Admin', 'group': ''},
            {'uuid': '54e63594-d520-42f0-8ec9-bbb3651fab43', 'name': 'cache_rd_dashboard_intraday',
                'id': 'prod.54e63594-d520-42f0-8ec9-bbb3651fab43',
                'project': 'Admin', 'group': ''}
        ]

        # same id, different names
        job_by_id = {'uuid': 'c7d3aea1-28af-4c14-9580-3792fe0e52f0',
            'name': 'cache_rd_dashboard_summary',
            'id': 'prod.c7d3aea1-28af-4c14-9580-3792fe0e52f0',
            'project': 'Admin', 'group': ''}
        job_by_id = find_job(jobs, job_by_id)
        assert job_by_id["id"] == 'prod.c7d3aea1-28af-4c14-9580-3792fe0e52f0'

        # different ids, same name
        job_by_name = {'uuid': '54e63594-d520-42f0-8ec9-bbb3651fab43',
            'name': 'cache_rd_dashboard_intraday',
            'id': 'prod.54e63594-d520-42f0-8ec9-bbb3651fab43',
            'project': 'Admin', 'group': ''}
        job_by_name = find_job(jobs, job_by_name)
        assert job_by_name["id"] == 'prod.54e63594-d520-42f0-8ec9-bbb3651fab43'

    def test_get_job_details(self):
        job_id = "a694aa5e-360c-4559-bcdf-1a97afb2cac1"
        env = "qa"
        job_details = get_job_details(
            env=env, job_id=job_id, live_data_source=DataSource.FILE_SYSTEM)
        print(job_details)
