"""Read information from all jobs"""
from runduck.datainteraction import DataSource
from runduck.datainteraction import DataInteraction
from runduck import app

def read_environment(live_data_source, force_refresh=False, env="qa"):
    """Iterate through projects to get the jobs and job details for one environment

    :param live_data_source: Where to get the data if not available in the cache
    :type live_data_source: DataSource
    :param force_refresh: Force reading from live_data_source, defaults to False
    :type force_refresh: bool, optional
    :param env: Which rundeck to read from, must match the key in the ENV configuration, defaults to "qa"
    :type env: str, optional
    :return: project with jobs
    :rtype: array of projects
    """

    interaction = DataInteraction(live_data_source=live_data_source, env=env)
    projects = interaction.get_data("projects").get("data")
    for project_i, project in enumerate(projects):
        print(f"[{env}] Reading jobs from {project_i + 1} of {len(projects)}: {project['name']}")
        jobs = interaction.get_data(
            "jobs",
            project=project["name"],
            force_refresh=force_refresh
        ).get("data")

        project["jobs"] = jobs

        for job_i, job in enumerate(jobs):
            print(f"Job {job_i + 1} of {len(jobs)}: {job['name']}")
            # print(f"  Reading metadata for {job['id']}")
            job_metadata = interaction.get_data(
                "job.metadata",
                jobid=job["id"],
                force_refresh=force_refresh
            ).get("data")
            job.update(job_metadata)

            # print(f"  Reading job definition for {job['id']}")
            job_definition = interaction.get_data(
                "job.definition",
                jobid=job["id"],
                force_refresh=force_refresh
            ).get("data")
            job.update(next(iter(job_definition)))

        # Update back the job list to make it easier to list with all the details
        interaction.set_redis("jobs", jobs, project=project["name"])

    return projects

def read_all_environments(live_data_source, force_refresh=False):
    """Read all data from all configured environments and merge into result dataset

    :param live_data_source: Where to get the data if not available in the cache
    :type live_data_source: DataSource
    :param force_refresh: Force reading from live_data_source, defaults to False
    :type force_refresh: bool, optional
    """
    environments = app.config["ENV"]
    env_data = None
    all_data = {}
    for env in environments:
        all_data[env] = read_environment(live_data_source, force_refresh=force_refresh, env=env)
    return all_data

