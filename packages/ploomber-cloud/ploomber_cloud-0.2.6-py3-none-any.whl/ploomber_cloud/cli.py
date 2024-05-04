import click

from ploomber_cloud import (
    api_key,
    deploy as deploy_,
    github as github_,
    init as init_,
    examples as examples_,
    delete as delete_,
    templates as templates_,
    resources as resources_,
    labels as labels_,
    __version__,
)
from ploomber_cloud.config import path_to_config


OPTIONS_CONFIG = ("--config", "-c")
OPTIONS_CONFIG_HELP = "Path to the config file to use. Defaults to ploomber-cloud.json"


@click.group()
@click.version_option(version=__version__)
def cli():
    pass


@cli.command()
@click.argument("key", type=str, required=True)
def key(key):
    """Set your API key"""
    api_key.set_api_key(key)


@cli.command()
@click.option(
    "--watch", is_flag=True, help="Track deployment status in the command line"
)
@click.option(
    "--watch-incremental",
    "watch_incremental",
    is_flag=True,
    help="Track incremental deployment logs in the command line",
)
@click.option(
    *OPTIONS_CONFIG,
    help=OPTIONS_CONFIG_HELP,
)
def deploy(watch, watch_incremental, config):
    """Deploy your project to Ploomber Cloud"""
    with path_to_config(config):
        deploy_.deploy(watch, watch_incremental)


@cli.command()
@click.option(
    "--project-id",
    "project_id",
    type=str,
    required=True,
)
@click.option(
    "--job-id",
    "job_id",
    type=str,
    required=False,
)
def watch(project_id, job_id):
    """Watch the deployment status of a project"""
    if not job_id:
        deploy_.watch(project_id)
    else:
        deploy_.watch(project_id, job_id)


@cli.command()
@click.option(
    "--from-existing",
    "from_existing",
    is_flag=True,
    help="Choose an existing project to initialize from",
)
@click.option(
    "--force",
    "-f",
    is_flag=True,
    default=None,
    help="Force initialize a project to override the config file",
)
@click.option(
    *OPTIONS_CONFIG,
    help=OPTIONS_CONFIG_HELP,
)
def init(from_existing, force, config):
    """Initialize a Ploomber Cloud project"""
    with path_to_config(config):
        init_.init(from_existing, force)


@cli.command()
def github():
    """Configure workflow file for triggering
    GitHub actions"""
    github_.github()


@cli.command()
@click.argument("name", type=str, required=False)
def examples(name):
    """Download an example from the doc repository"""
    examples_.examples(name)


@cli.command()
@click.option("--project-id", "project_id", help="Project ID to delete", required=False)
@click.option(
    "--all",
    "-a",
    is_flag=True,
    default=None,
    help="Option to delete all projects",
)
def delete(project_id, all):
    """Delete a project or all projects"""
    if all:
        delete_.delete_all()
    elif project_id:
        delete_.delete(project_id)
    else:
        delete_.delete()


@cli.command()
@click.argument("name", type=str)
@click.option(
    *OPTIONS_CONFIG,
    help=OPTIONS_CONFIG_HELP,
)
def templates(name, config):
    """Configure a project using a template"""
    with path_to_config(config):
        templates_.template(name)


@cli.command()
@click.option(
    "--force",
    "-f",
    is_flag=True,
    default=None,
    help="Force configure resources to override the config file",
)
@click.option(
    *OPTIONS_CONFIG,
    help=OPTIONS_CONFIG_HELP,
)
def resources(force, config):
    """Configure project resources"""
    with path_to_config(config):
        resources_.resources(force)


@cli.command()
@click.option(
    "--add",
    "-a",
    multiple=True,
    type=str,
    default=[],
    help="Add labels to the project",
)
@click.option(
    "--delete",
    "-d",
    multiple=True,
    type=str,
    default=[],
    help="Delete project labels",
)
@click.option(
    *OPTIONS_CONFIG,
    help=OPTIONS_CONFIG_HELP,
)
def labels(add, delete, config):
    """Add project labels"""
    with path_to_config(config):
        labels_.labels(list(add), list(delete))


if __name__ == "__main__":
    cli()
