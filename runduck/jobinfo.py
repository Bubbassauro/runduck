"""Read information from all jobs"""
import pandas as pd
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

def find_project(project_to_find, projects):
    """Find matching project in the list"""
    for proj in projects:
        if project_to_find["name"] == proj["name"]:
            return proj
    return None

def merge_jobs(jobs1, jobs2, env1, env2):
    """Merge two lists of jobs
    
    :param jobs1: list of jobs from first environment
    :type jobs1: list of objects
    :param jobs2: list of jobs from second environment
    :type jobs2: list of objects
    :param env1: name of the first environment for column suffix
    :type env1: string
    :param env2: name of the second environment for column suffix
    :type env2: string

    :returns: DataFrame with combined jobs, matched by id + 
        matched by name that were not matched by id
    """
    df_jobs1 = pd.DataFrame(jobs1)
    df_jobs2 = pd.DataFrame(jobs2)

    if df_jobs1.empty:
        return df_jobs2
    if df_jobs2.empty:
        return df_jobs1

    # matched by id (priority)
    id_match = pd.merge(
        df_jobs1, df_jobs2,
        how="inner",
        on=("project", "group", "id"),
        suffixes=(f"_{env1}", f"_{env2}")
    )

    # matched by name
    name_match = pd.merge(
        df_jobs1, df_jobs2,
        how="outer",
        on=("project", "group", "name"),
        suffixes=(f"_{env1}", f"_{env2}")
    )
    pd.set_option('display.max_rows', None)
    name_except_id = (name_match[
        (~name_match[f"id_{env1}"].isin(id_match["id"].to_list())) & 
        (~name_match[f"id_{env2}"].isin(id_match["id"].to_list()))
    ])
    # final is matched by id + matched by name that were not matched by id
    matches = pd.concat([id_match, name_except_id], ignore_index=True)
    
    # make column names lowercase
    cols = {col: col.lower() for col in matches.columns.to_list()}
    matches.rename(columns=cols, inplace=True)
    return matches

def combine_data(live_data_source, force_refresh=False):
    """Read all the data and join
    
    :param live_data_source: Where to get the data if not available in the cache
    :type live_data_source: DataSource
    :param force_refresh: Force reading from live_data_source, defaults to False
    :type force_refresh: bool, optional
    """
    environments = app.config["ENV"]
    env1 = "qa"
    env2 = "prod"
    interaction1 = DataInteraction(live_data_source=live_data_source, env=env1)
    projects1 = interaction1.get_redis("projects")

    interaction2 = DataInteraction(live_data_source=live_data_source, env=env2)
    projects2 = interaction1.get_redis("projects")

    df1 = pd.DataFrame(projects1)
    df2 = pd.DataFrame(projects2)
    combined = pd.merge(
        df1, df2,
        how="outer",
        on="name",
        suffixes=(f"_{env1}", f"_{env2}")
    )
    combined.fillna("", inplace=True)

    project_list = combined.to_dict(orient='record')
    # print(project_list)
    # project = next(iter(project_list))
    # jobs1 = interaction1.get_redis("jobs", project="App-Integrations")
    # jobs2 = interaction2.get_redis("jobs", project="App-Integrations")
    # combined_jobs = merge_jobs(jobs1, jobs2, env1, env2)
    # print(combined_jobs)
    for project in project_list:
        # print(project["name"], "=" * 30)
        jobs1 = interaction1.get_redis("jobs", project=project["name"])
        jobs2 = interaction2.get_redis("jobs", project=project["name"])
        combined_jobs = merge_jobs(jobs1, jobs2, env1, env2)

        project["jobs"] = combined_jobs.dropna().to_dict(orient="record")

    # # Save combined data
    interaction_all = DataInteraction(live_data_source=DataSource.API, env="all")
    interaction_all.set_redis("projects", project_list)
