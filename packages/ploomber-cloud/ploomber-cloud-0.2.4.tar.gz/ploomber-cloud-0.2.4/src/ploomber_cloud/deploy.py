import click
import time
import json
from os import environ

from ploomber_core.exceptions import modify_exceptions

from ploomber_cloud.exceptions import (
    BasePloomberCloudException,
    InvalidPloomberResourcesException,
)
from ploomber_cloud import api, zip_
from ploomber_cloud.config import PloomberCloudConfig
from ploomber_cloud.github import display_github_workflow_info_message
from ploomber_cloud._telemetry import telemetry
from ploomber_cloud.util import print_divider
from ploomber_cloud.resources import _get_resource_choices

STATUS_COLOR = {
    "pending": "white",
    "active": "yellow",
    "finished": "green",
    "success": "green",
    "failed": "red",
    "inactive": "red",
    "stopped": "magenta",
}

FAILED_STATUSES = (
    "docker-failed",
    "provisioning-failed",
    "infrastructure-failed",
    "failed",
)

INTERVAL_SECS = 15.0
TIMEOUT_MINS = 15.0


def _unpack_job_status(job):
    """
    Format and output a job status message.
    Return job status (and URL if success).

    Parameters
    ----------
    job: JSON
        Contains job status information to output and process.

    Returns
    ----------
    job_status: str
        Status of job. Possible values: "success", "running", or "failed".

    app_url: str
        URL to view dashboard. Only returned if job_status == "success".
    """
    tasks = job["summary"]
    status_msg = []

    for name, status in tasks:
        status_msg.append(f"{name}: {click.style(status, fg=STATUS_COLOR[status])} | ")

    click.echo("".join(status_msg))

    # grab job status as reported by backend api
    status = job["status"]

    # job is running and reporting healthy
    if status == "running":
        return "success", job["resources"]["webservice"]

    # job has failed or stopped
    if status in FAILED_STATUSES:
        return "failed", None

    # job is still pending, continue watching
    return "pending", None


def _watch(client, project_id, job_id):
    """Display status bar and logs of project deployment"""
    start_time = time.time()
    interval = INTERVAL_SECS
    timeout = 60.0 * TIMEOUT_MINS

    # poll every 'interval' secs until 'timeout' mins
    while True:
        status_page = api.PloomberCloudEndpoints().status_page(project_id, job_id)

        curr_time = time.time()
        time_diff = curr_time - start_time

        if time_diff >= timeout:
            click.secho("Timeout reached.", fg="yellow")
            click.echo(f"For more details, go to: {status_page}")
            return

        # get job status and logs from API
        job = client.get_job_by_id(job_id)
        logs = client.get_job_logs_by_id(job_id)

        # decide which logs to show based on status
        logs_to_show = "build-docker"
        # if deploy-docker is finished, show webservice logs
        if job["summary"][1][1] in ("success", "finished"):
            logs_to_show = "webservice"

        curr_time_formatted = time.strftime("%H:%M:%S", time.localtime(curr_time))

        # Display link to status page, status bar, and logs
        click.clear()
        click.echo(
            f"[{curr_time_formatted}] \
Deploying project: {project_id} with job ID: {job_id}..."
        )
        print_divider()
        click.echo(f"Web status page: {status_page}")
        print_divider()
        job_status, app_url = _unpack_job_status(job)
        print_divider()
        click.echo(f"Showing {logs_to_show} logs...")
        print_divider()
        click.echo(logs["logs"][logs_to_show])

        # deploy has either succeeded or failed
        if job_status != "pending":
            click.secho(f"Deployment {job_status}.", fg=STATUS_COLOR[job_status])
            click.echo(f"View project dashboard: {status_page}")
            if job_status == "success":
                click.echo(f"View your deployed app: {app_url}")
            break

        time.sleep(interval - (time_diff % interval))


def generate_secrets_from_env(keys):
    """
    From a list of keys, read the value of each one and
    package the key-value pairs into a JSON string.

    For this to work, the secrets must be defined as
    environment variables.
    """
    secrets_arr = []
    output_message = [
        "Adding the following secrets to the app: ",
    ]

    for key in keys:
        value = environ.get(key)
        if not value:
            raise BasePloomberCloudException(
                f"Value for key '{key}' not found. "
                f"Set the value using 'export {key}=value' "
                "or remove it from 'secret-keys'"
            )
        secrets_arr.append({"key": key, "value": value})
        output_message.append(f"{key}, ")

    click.echo("".join(output_message))
    return json.dumps(secrets_arr)


def check_for_secrets_in_config(secret_keys, secrets):
    """
    Check if secrets are defined in `.env` or `secret-keys`.
    If defined in both, returns an error.

    Parameters
    ----------
    secret_keys: list
        A list of keys (strings) of environment variables to be read
        from the current environment.
        It is only keys/names, not the values.

    secrets: JSON
        A list of key-value pairs from .env as a JSON string.
        If no secrets defined in .env, secrets is None.

    Returns
    ----------
    secrets: JSON
        A list of key-value pairs as a JSON string.
    """
    if secret_keys and secrets:
        raise BasePloomberCloudException(
            "Found 'secret-keys' section and '.env' file. "
            "Only one method for adding secrets may be used.\n"
            "Delete '.env' or remove 'secret-keys' from 'ploomber-cloud.json'."
        )
    elif secret_keys:
        click.echo("Generating secrets from 'secret-keys' and environment variables.")
        return generate_secrets_from_env(secret_keys)

    return secrets


@modify_exceptions
@telemetry.log_call(log_args=True)
def deploy(watch):
    """Deploy a project to Ploomber Cloud, requires a project to be initialized"""

    client = api.PloomberCloudClient()
    config = PloomberCloudConfig()
    config.load()

    with zip_.zip_app(verbose=True) as (path_to_zip, secrets):
        secrets = check_for_secrets_in_config(config.data.get("secret-keys"), secrets)
        click.echo(f"Deploying project with id: {config.data['id']}...")
        try:
            output = client.deploy(
                path_to_zip=path_to_zip,
                project_type=config.data["type"],
                project_id=config.data["id"],
                secrets=secrets,
                resources=config.data.get("resources"),
                template=config.data.get("template"),
                labels=config.data.get("labels"),
            )
        except BasePloomberCloudException as e:
            if "Invalid Resource" in e.get_message():
                cpu_options, ram_options, gpu_options = _get_resource_choices()
                cpu_options = [float(opt) for opt in cpu_options]
                ram_options = [int(float(opt)) for opt in ram_options]

                raise InvalidPloomberResourcesException(
                    "Resource choices are invalid.\n"
                    f"Valid CPU options: {cpu_options}\n"
                    f"Valid RAM options: {ram_options}\n"
                    f"Valid GPU options: {gpu_options}"
                ) from e
            else:
                raise
        if watch:
            _watch(client, output["project_id"], output["id"])

    display_github_workflow_info_message()


@modify_exceptions
@telemetry.log_call(log_args=True)
def watch(project_id, job_id=None):
    """Watch the deployment status of a project"""
    client = api.PloomberCloudClient()
    if not job_id:
        project = client.get_project_by_id(project_id)
        job_id = project["jobs"][0]["id"]

    _watch(client, project_id, job_id)
