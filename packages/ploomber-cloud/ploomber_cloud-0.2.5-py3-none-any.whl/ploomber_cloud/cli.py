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
def deploy(watch, watch_incremental):
    """Deploy your project to Ploomber Cloud"""
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
def init(from_existing, force):
    """Initialize a Ploomber Cloud project"""
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
def templates(name):
    """Configure a project using a template"""
    templates_.template(name)


@cli.command()
@click.option(
    "--force",
    "-f",
    is_flag=True,
    default=None,
    help="Force configure resources to override the config file",
)
def resources(force):
    """Configure project resources"""
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
def labels(add, delete):
    """Add project labels"""
    labels_.labels(list(add), list(delete))


if __name__ == "__main__":
    cli()
