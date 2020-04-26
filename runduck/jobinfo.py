"""Read information from all jobs"""
from datetime import datetime
from cron_descriptor import get_description
from runduck.datainteraction import DataSource
from runduck.datainteraction import DataInteraction
from runduck import app
from runduck.utils import get_elapsed_time
from runduck.utils import get_object_property
from runduck.utils import get_cron


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
        print(
            f"[{env}] Reading jobs from {project_i + 1} of {len(projects)}: {project['name']}"
        )
        jobs = interaction.get_data(
            "jobs", project=project["name"], force_refresh=force_refresh
        ).get("data")

        project["jobs"] = jobs

        for job_i, job in enumerate(jobs):
            # print(f"Job {job_i + 1} of {len(jobs)}: {job['name']}")
            # print(f"  Reading metadata for {job['id']}")
            job_metadata = interaction.get_data(
                "job.metadata", jobid=job["id"], force_refresh=force_refresh
            ).get("data")
            job.update(job_metadata)

            # print(f"  Reading job definition for {job['id']}")
            job_definition = interaction.get_data(
                "job.definition", jobid=job["id"], force_refresh=force_refresh
            ).get("data")
            job.update(next(iter(job_definition)))

    return projects


def read_all_environments(live_data_source=DataSource.API, force_refresh=False):
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
        all_data[env] = read_environment(
            live_data_source, force_refresh=force_refresh, env=env
        )
    return all_data


def append_info(job, project, env, env_order):
    """Add project and environment info
    Also include:
        env : environement
        euid : environment.id (id that's unique in all environments)
    """
    job_info = {}
    # copy fields that we will need from job
    fields_to_include = [
        "uuid",
        "group",
        "name",
        "scheduleEnabled",
        "executionEnabled",
        "description",
        "permalink",
    ]
    for field in fields_to_include:
        job_info[field] = job.get(field)

    job_info["project_name"] = project["name"]
    job_info["project_description"] = project["description"]
    job_info["env"] = env
    job_info["env_order"] = env_order
    job_info["id"] = f"{env}.{job['id']}"

    job_info["cron"] = get_cron(job.get("schedule"))
    if job_info.get("cron"):
        try:
            job_info["schedule_description"] = get_description(job_info["cron"])
        except:
            CRED = "\33[31m"
            CEND = "\033[0m"
            print(
                CRED,
                f"\nError getting schedule description for {project['name']} / {job['group']} / {job['name']}",
                CEND,
            )
            print(job.get("cron"))

    return job_info


def find_job(jobs, job_to_find):
    """Find matching job in list"""
    for job in jobs:
        if job["uuid"] == job_to_find["uuid"]:
            return job
        if (
            job["project_name"] == job_to_find["project_name"]
            and job["group"] == job_to_find["group"]
            and job["name"] == job_to_find["name"]
        ):
            return job
    return None


def get_job_details(env, job_id, live_data_source=DataSource.API, force_refresh=False):
    """Get details of one job"""
    interaction = DataInteraction(live_data_source=live_data_source, env=env)
    job_metadata = interaction.get_data(
        "job.metadata", force_refresh=force_refresh, jobid=job_id
    ).get("data")

    job_definition = interaction.get_data(
        "job.definition", force_refresh=force_refresh, jobid=job_id
    ).get("data")
    job_metadata.update(next(iter(job_definition)))
    return job_metadata


def get_last_execution(
    env, job_id, live_data_source=DataSource.API, force_refresh=False
):
    interaction = DataInteraction(live_data_source=live_data_source, env=env)
    response = interaction.get_data(
        "job.executions",
        force_refresh=force_refresh,
        jobid=job_id,
        max=1,  # only using the last execution for now
    ).get("data")
    if get_object_property(response, "paging.count", 0) > 0:
        execution = next(iter(response["executions"]))

        # Append duration
        execution["duration"] = get_elapsed_time(
            get_object_property(execution, "date-started.date"),
            get_object_property(execution, "date-ended.date"),
        )
        return execution
    return {}


def combine_data(force_refresh=False):
    raw_data = read_all_environments(force_refresh=force_refresh)
    all_jobs = []

    # go over each environment
    for index, env in enumerate(raw_data):
        print(f"processing {index}: {env}")
        for project in raw_data[env]:
            for job in project["jobs"]:
                job_info = append_info(
                    job=job, project=project, env=env, env_order=index
                )
                parent_job = find_job(all_jobs, job_info)
                if parent_job:
                    job_info["parentId"] = parent_job["id"]
                else:
                    job_info["parentId"] = None
                    # print(f"added to all jobs {job['euid']}")

                # sort by parent job name
                job_info["sortkey"] = (
                    f"{job_info.get('project_name')} "
                    f"{job_info.get('group')} "
                    f"{parent_job['name'] if parent_job else job_info.get('name')} "
                    f"{job_info['env_order']}"
                )
                all_jobs.append(job_info)

    # sort data
    all_jobs = sorted(all_jobs, key=lambda item: f"{item.get('sortkey')}")

    interaction = DataInteraction()
    interaction.set_redis("combined", all_jobs)
    print("DONE!")
