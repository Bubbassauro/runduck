"""Read information from all jobs"""
from runduck.datainteraction import DataSource
from runduck.datainteraction import DataInteraction


def read_all_data(live_data_source, force_refresh=False):
    interaction = DataInteraction(live_data_source=live_data_source)
    projects = interaction.get_data("projects").get("data")
    for project_i, project in enumerate(projects):
        print(
            f"\nReading jobs from {project_i + 1} of {len(projects)}: {project['name']}",
            "=" * 30,
        )
        jobs = interaction.get_data(
            "jobs",
            project=project["name"],
            force_refresh=force_refresh
        ).get("data")

        project["jobs"] = jobs
        for job_i, job in enumerate(jobs):
            print(f"Job {job_i + 1} of {len(jobs)}: {job['name']}")
            print(f"  Reading metadata for {job['id']}")
            job_metadata = interaction.get_data(
                "job.metadata",
                jobid=job["id"],
                force_refresh=force_refresh
            ).get("data")
            job["metadata"] = job_metadata

            print(f"  Reading job definition for {job['id']}")
            job_definition = interaction.get_data(
                "job.definition",
                jobid=job["id"],
                force_refresh=force_refresh
            ).get("data")
            job["definition"] = job_definition

    return projects
