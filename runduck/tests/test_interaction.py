"""Test the datareader class
python -m pytest -v -s
"""
import unittest
import pytest
from runduck import app
from runduck.datainteraction import DataSource
from runduck.datainteraction import DataInteraction


class DataReaderTestCase(unittest.TestCase):
    """Tests for bo_helpers module"""

    # pylint:disable=R0201
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        app.config.from_pyfile("../app.cfg")
        self.interaction = DataInteraction(live_data_source=DataSource.FILE_SYSTEM)

    def test_get_redis(self):
        data = self.interaction.get_redis("projects")
        # print(data)
        assert data

    def test_get_filesystem_projects(self):
        data = self.interaction.get_filesystem("projects")
        assert data

    def test_get_filesystem_jobs(self):
        data = self.interaction.get_filesystem("jobs", project="App-Integrations")
        assert data

    def test_get_filesystem_metadata(self):
        data = self.interaction.get_filesystem(
            "job.metadata", jobid="a694aa5e-360c-4559-bcdf-1a97afb2cac1"
        )
        assert data

    def test_get_filesystem_definition(self):
        data = self.interaction.get_filesystem(
            "job.definition", jobid="a694aa5e-360c-4559-bcdf-1a97afb2cac1"
        )
        assert data

    def test_redis_save(self):
        data = self.interaction.get_filesystem("projects")
        self.interaction.set_redis("projects", data)

    @pytest.mark.skip
    def test_api(self):
        projects = self.interaction.get_api("projects")
        print(projects)
        assert projects

    def test_clear_redis(self):
        data = self.interaction.get_filesystem("projects")
        self.interaction.set_redis("projects", data)
        self.interaction.clear_redis("projects")
        data_redis = self.interaction.get_redis("projects")
        assert not data_redis

    def test_get_data(self):
        # start with a clear cache
        self.interaction.clear_redis("projects")
        data_fs = self.interaction.get_data("projects")
        assert data_fs["source"] == DataSource.FILE_SYSTEM.value
        # Now the data should be in redis
        data_redis = self.interaction.get_data("projects")
        assert data_redis["source"] == DataSource.REDIS.value
        # both should have the same info
        assert data_fs["data"] == data_redis["data"]
