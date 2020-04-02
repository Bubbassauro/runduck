"""Read data from Redis, or sample file, or API"""
import os
import json
import yaml
import redis
import requests
import jsonpickle
from enum import Enum
from runduck import app


class DataSource(Enum):
    """File system is used for local (disconnected) tests"""

    API = "api"
    FILE_SYSTEM = "fs"
    REDIS = "redis"


class DataInteraction(object):
    """Common object to read data from redis or from file system or API"""

    def __init__(self, live_data_source=DataSource.API, env="qa"):
        """
        :live_data_source: Once of the DataSource types, defaults to API. Pass FILE_SYSTEM to read from sample data when developing / testing
        :env: Environment to read from (qa/prod)
        """
        self.CONFIG = {
            "projects": {
                "format": "json",
                DataSource.API: "/api/1/projects",
                DataSource.FILE_SYSTEM: "{env}.projects.json",
                DataSource.REDIS: {"key": "runduck:{env}", "field": "projects"},
            },
            "jobs": {
                "format": "json",
                DataSource.API: "/api/14/project/{project}/jobs",
                DataSource.FILE_SYSTEM: "{env}.project.{project}.jobs.json",
                DataSource.REDIS: {
                    "key": "runduck:{env}:projects:{project}",
                    "field": "jobs",
                },
            },
            "job.metadata": {
                "format": "json",
                DataSource.API: "/api/18/job/{jobid}/info",
                DataSource.FILE_SYSTEM: "{env}.job.{jobid}.metadata.json",
                DataSource.REDIS: {
                    "key": "runduck:{env}:jobs:{jobid}",
                    "field": "metadata",
                },
            },
            "job.definition": {
                "format": "yaml",
                DataSource.API: "/api/1/job/{jobid}",
                DataSource.FILE_SYSTEM: "{env}.job.{jobid}.definition.yaml",
                DataSource.REDIS: {
                    "key": "runduck:{env}:jobs:{jobid}",
                    "field": "definition",
                },
            },
            # This is where all the combined data for the API will be stored (redis only)
            "combined": {
                "format": "json",
                DataSource.REDIS: {"key": "runduck:all", "field": "combined"},
            },
        }

        self.pool = redis.ConnectionPool(
            host=app.config["REDIS_HOST"],
            port=app.config["REDIS_PORT"],
            db=app.config["REDIS_INDEX"],
        )
        self.redis = redis.StrictRedis(connection_pool=self.pool, decode_responses=True)
        self.live_data_source = live_data_source
        self.env = env

    def prepare_args(self, **args):
        """Add env value to arguments"""
        if not args:
            args = {}
        args.update({"env": self.env})
        return args

    def get_filesystem(self, data_key, **args):
        """Read data from sample json file"""
        args = self.prepare_args(**args)

        base_path = os.path.dirname(os.path.abspath(__file__))
        file_name = self.CONFIG[data_key][DataSource.FILE_SYSTEM].format(**args)
        file_path = f"{base_path}/sampledata/{file_name}"
        parsed_data = {}
        with open(file_path, "rb") as file_obj:
            if self.CONFIG[data_key]["format"] == "json":
                parsed_data = json.load(file_obj)
            elif self.CONFIG[data_key]["format"] == "yaml":
                parsed_data = yaml.safe_load(file_obj)
            else:
                raise ValueError(
                    f"{self.CONFIG[data_key]['format']} is not a valid file format"
                )
            file_obj.close()
        return parsed_data

    def get_api(self, data_key, **args):
        """Call Rundeck API"""
        base_url = app.config["ENV"][self.env]["base_url"].strip("/")

        headers = {}
        params = args if args else {}
        params["authtoken"] = app.config["ENV"][self.env]["authtoken"]
        response_format = self.CONFIG[data_key]["format"]

        if response_format == "json":
            headers["Accept"] = "application/json"
        elif response_format == "yaml":
            params["format"] = "yaml"

        url = f"{base_url}{self.CONFIG[data_key][DataSource.API]}".format(**params)
        print(url, params)
        resp = requests.get(url, headers=headers, params=params)
        resp.raise_for_status()
        if response_format == "json":
            return resp.json()
        else:
            # print(str(resp.content))
            return yaml.safe_load(resp.content)

    def get_redis(self, data_key, **args):
        """Get data from redis data source"""
        args = self.prepare_args(**args)
        key = self.CONFIG[data_key][DataSource.REDIS]["key"].format(**args)
        field = self.CONFIG[data_key][DataSource.REDIS]["field"]

        raw_data = self.redis.hget(key, field)
        if raw_data is None:
            return None

        data = jsonpickle.decode(raw_data)
        return data

    def set_redis(self, data_key, value, **args):
        """Add value to redis cache"""
        args = self.prepare_args(**args)
        key = self.CONFIG[data_key][DataSource.REDIS]["key"].format(**args)
        field = self.CONFIG[data_key][DataSource.REDIS]["field"]
        self.redis.hset(key, field, jsonpickle.encode(value))

    def clear_redis_pattern(self, pattern):
        """Clear all matching redis keys"""
        keys = self.redis.keys(pattern)
        if keys:
            self.redis.delete(*keys)

    def clear_redis(self, data_key, **args):
        """Build the pattern and clear"""
        args = self.prepare_args(**args)
        pattern = self.CONFIG[data_key][DataSource.REDIS]["key"].format(**args)
        print("\n", pattern)
        self.clear_redis_pattern(pattern)

    def get_data(self, data_key, force_refresh=False, **args):
        """Get all the data under a key or call the source to get the data"""
        if not force_refresh:
            source = str(DataSource.REDIS)
            data = self.get_redis(data_key, **args)
            if not data is None:
                return {"source": DataSource.REDIS.value, "data": data}

        source = self.live_data_source
        if self.live_data_source == DataSource.FILE_SYSTEM:
            data = self.get_filesystem(data_key, **args)
        else:
            data = self.get_api(data_key, **args)

        self.set_redis(data_key, data, **args)

        return {"source": source.value, "data": data}
