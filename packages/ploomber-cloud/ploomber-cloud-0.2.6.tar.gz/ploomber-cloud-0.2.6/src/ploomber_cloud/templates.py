"""
Configure a project from a template
"""

from pathlib import Path
from string import Template
from importlib import resources
import secrets
from dotenv import dotenv_values

import requests
import click

from ploomber_cloud.assets import vllm as vllm_resources
from ploomber_cloud.config import PloomberCloudConfig
from ploomber_cloud.util import pretty_print
from ploomber_cloud.exceptions import BasePloomberCloudException
from ploomber_cloud import init, deploy
from ploomber_cloud import io


def validate_model_name(model_name):
    """Verify that HF model exists by name"""
    response = requests.get(f"https://huggingface.co/api/models/{model_name}")

    if response.ok:
        return {"exists": True, "gated": False}
    else:
        output = response.json()
        error_message = output.get("error", {})

        if "gated" in error_message:
            return {"exists": True, "gated": True}
        else:
            return {"exists": False, "gated": False}


def has_access_to_model(model_name, hf_token):
    """Verify user has access to HF model"""
    response = requests.get(
        f"https://huggingface.co/api/models/{model_name}",
        headers={"authorization": "Bearer {}".format(hf_token)},
    )
    return response.ok


def prompt_model_name(text):
    """Prompt user for model name"""
    model_name = click.prompt(text, default="facebook/opt-125m")
    response = validate_model_name(model_name)

    while not response["exists"]:
        click.secho(f"Model {model_name} not found, please try again.", fg="red")
        model_name = click.prompt(text, default="facebook/opt-125m")
        response = validate_model_name(model_name)

    return model_name, response["gated"]


def prompt_hf_token(model_name):
    """Prompt user for huggingface token"""
    hf_token = click.prompt("Enter your HF_TOKEN")

    while not has_access_to_model(model_name, hf_token):
        click.secho(
            f"The HF_TOKEN provided doesn't have access to {model_name}, please "
            "try again.",
            fg="red",
        )
        hf_token = click.prompt("Enter your HF_TOKEN")

    return hf_token


def get_parameters_and_token():
    """Get model name and hf_token for vllm"""
    model_name, gated = prompt_model_name("Model to serve via vLLM")
    hf_token = None

    if gated:
        click.secho(f"Model {model_name} is gated! Provide an HF_TOKEN", fg="yellow")
        hf_token = prompt_hf_token(model_name)

    params = {
        "MODEL_NAME": model_name,
    }

    return params, hf_token


def generate_env(hf_token):
    """Generate .env file for vllm template"""
    env_data = {"VLLM_API_KEY": secrets.token_urlsafe()}

    if hf_token:
        env_data["HF_TOKEN"] = hf_token

    click.echo("API KEY saved to .env file")

    env = "\n".join([f"{k}={v}" for k, v in env_data.items()])

    return {"mapping": env_data, "text": env}


def vllm():
    """Download and deploy vllm template app"""
    if any(Path.cwd().iterdir()):
        raise click.ClickException("This command must be run in an empty directory.")

    dockerfile_template = Template(resources.read_text(vllm_resources, "Dockerfile"))
    params, hf_token = get_parameters_and_token()
    dockerfile = dockerfile_template.substitute(**params)
    requirements = resources.read_text(vllm_resources, "requirements.txt")

    # TODO: update docs, show CLI guide, mention that vlLM requires a gpu and
    # that we have a trial
    env = generate_env(hf_token)
    Path(".env").write_text(env["text"])

    api_key = env["mapping"]["VLLM_API_KEY"]
    click.secho(f"Generated API key: {api_key}", fg="green")

    Path("Dockerfile").write_text(dockerfile)
    Path("requirements.txt").write_text(requirements)
    click.echo("Dockerfile and requirements.txt created")

    init.init(from_existing=False, force=False, project_type="docker")

    config = PloomberCloudConfig()
    config.load()
    config["resources"] = {"cpu": 4.0, "ram": 12, "gpu": 1}

    test_script_template = Template(resources.read_text(vllm_resources, "test-vllm.py"))
    test_script = test_script_template.substitute(
        API_KEY=api_key,
        APP_ID=config.data["id"],
    )

    Path("test-vllm.py").write_text(test_script)

    confirmation = click.confirm("Do you want to deploy now?", default=True)

    click.secho(
        "test-vllm.py created, once vLLM is running, test it with python test-vllm.py",
        fg="green",
    )

    if not confirmation:
        click.secho(
            "Deployment cancelled. You can deploy with: ploomber-cloud deploy",
            fg="yellow",
        )
        return
    else:
        deploy.deploy(watch=False)
        click.secho("Deployment started, should take about 12 minutes.", fg="green")


def validate_auth_issues_base_url(value):
    if value.startswith("https://"):
        return io.ValidationResult(
            is_valid=True,
            error_message=None,
            value_validated=value,
        )
    else:
        # the auth0 console doesn't show the protocol, so we add it in case the
        # user copied and paste the value
        if (
            ".auth0.com" in value
            and not value.startswith("https://")
            and not value.startswith("http://")
        ):
            return io.ValidationResult(
                is_valid=True,
                error_message=None,
                value_validated=f"https://{value}",
            )

        return io.ValidationResult(
            is_valid=False,
            error_message="must start with https://",
            value_validated=None,
        )


def auth0():
    """Configure auth0 for an existing project"""
    # Check for init, if not, prompt and run init flow
    if not Path("ploomber-cloud.json").exists():
        run_init = click.confirm(
            "Project must be initialized to continue. Would you like to initialize?"
        )

        if not run_init:
            raise BasePloomberCloudException(
                "This command requires a ploomber-cloud.json file.\n"
                "Run 'ploomber-cloud init' to initialize your project."
            )

        init.init(from_existing=False, force=False)

    # Prompt for secrets
    auth0_secrets = {
        "AUTH_CLIENT_ID": None,
        "AUTH_ISSUER_BASE_URL": None,
    }

    validators = {"AUTH_ISSUER_BASE_URL": validate_auth_issues_base_url}

    for key in auth0_secrets.keys():
        auth0_secrets[key] = io.prompt(
            validator=validators.get(key),
            text=f"Enter the value for {key}",
        )

    auth0_secrets["AUTH_SECRET"] = secrets.token_urlsafe()

    # Check for `.env` and load secrets if they exist
    final_secrets = {}

    if Path(".env").exists():
        final_secrets = dotenv_values(".env")

    # Add user-input secrets. Overrides keys if they already exist.
    final_secrets.update(auth0_secrets)

    # Write old and new secrets to .env
    with open(".env", "w") as env_file:
        for key, value in final_secrets.items():
            env_file.write(f"{key}={value}\n")

    # Add `node-auth0` under `template` in pcloud json
    config = PloomberCloudConfig()
    config.load()
    config["template"] = "node-auth0"

    # Display message to deploy
    click.echo("Successfully configured auth0. To deploy, run 'ploomber-cloud deploy'")


ALLOWED_TEMPLATES = {"vllm": vllm, "auth0": auth0}


def template(name):
    """Call template command according to name"""
    if name not in ALLOWED_TEMPLATES.keys():
        raise click.ClickException(
            f"Template {name} not found. Valid options: "
            f"{pretty_print(ALLOWED_TEMPLATES)}"
        )

    ALLOWED_TEMPLATES[name]()
