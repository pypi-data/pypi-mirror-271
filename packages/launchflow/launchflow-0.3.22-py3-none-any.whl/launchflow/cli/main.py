import asyncio
import os
from typing import List, Optional

import beaupy
import fsspec
import rich
import typer
import uvloop
from launchflow.aws.ecs_fargate import ECSFargate
from launchflow.cli import project_gen
from launchflow.cli.accounts import account_commands
from launchflow.cli.ast_search import (
    find_launchflow_resources,
    find_launchflow_services,
)
from launchflow.cli.config import config_commands
from launchflow.cli.constants import (
    API_KEY_HELP,
    ENVIRONMENT_HELP,
    PROJECT_HELP,
    SCAN_DIRECTORY_HELP,
    SERVICE_HELP,
)
from launchflow.cli.environments import environment_commands
from launchflow.cli.gen.templates.django.django_template import DjangoProjectGenerator
from launchflow.cli.gen.templates.fastapi.fastapi_template import (
    FastAPIProjectGenerator,
)
from launchflow.cli.gen.templates.flask.flask_template import FlaskProjectGenerator
from launchflow.cli.project import project_commands
from launchflow.cli.resources import resource_commands
from launchflow.cli.secrets import secret_commands
from launchflow.cli.services import service_commands
from launchflow.cli.utils import print_response
from launchflow.cli.utyper import UTyper
from launchflow.clients.client import LaunchFlowAsyncClient
from launchflow.clients.response_schemas import ProjectResponse
from launchflow.config import config
from launchflow.config.launchflow_yaml import ServiceConfig
from launchflow.exceptions import LaunchFlowRequestFailure
from launchflow.flows.account_id import get_account_id_from_config
from launchflow.flows.auth import login_flow, logout_flow
from launchflow.flows.cloud_provider import CloudProvider
from launchflow.flows.cloud_provider import connect as connect_provider
from launchflow.flows.environments_flows import get_environment
from launchflow.flows.project_flows import get_project
from launchflow.flows.resource_flows import clean as clean_resources
from launchflow.flows.resource_flows import create as create_resources
from launchflow.flows.resource_flows import destroy as destroy_resources
from launchflow.flows.resource_flows import (
    import_resources,
    is_local_resource,
    stop_local_containers,
)
from launchflow.flows.service_flows import deploy as deploy_services
from launchflow.flows.service_flows import import_services
from launchflow.gcp.cloud_run import CloudRun
from launchflow.service import Service
from rich.console import Console
from rich.panel import Panel

import launchflow
from launchflow.clients import async_launchflow_client_ctx

app = UTyper(help="LaunchFlow CLI.")
app.add_typer(account_commands.app, name="accounts")
app.add_typer(project_commands.app, name="projects")
app.add_typer(environment_commands.app, name="environments")
app.add_typer(resource_commands.app, name="resources")
app.add_typer(service_commands.app, name="services")
app.add_typer(config_commands.app, name="config")
app.add_typer(secret_commands.app, name="secrets")


async def _get_project_info(
    client: LaunchFlowAsyncClient,
    project_name: Optional[str] = None,
    prompt_for_creation: bool = True,
):
    # This check replaces the cli project arg with the configured project (if set)
    if project_name is None:
        project_name = config.project
    # Fetches the latest project info from the server
    return await get_project(
        client, project_name=project_name, prompt_for_creation=prompt_for_creation
    )


async def _get_environment_info(
    client: LaunchFlowAsyncClient,
    project: ProjectResponse,
    environment_name: Optional[str] = None,
    prompt_for_creation: bool = True,
):
    # This check replaces the cli env arg with the configured environment (if set)
    if environment_name is None:
        environment_name = config.environment
    # Fetches the latest environment info from the server
    return await get_environment(
        client=client,
        project=project,
        environment_name=environment_name,
        prompt_for_creation=prompt_for_creation,
    )


def _get_service_infos(service_name: Optional[str] = None) -> List[ServiceConfig]:
    service_configs = config.list_service_configs()
    if service_name is None:
        return service_configs
    if service_name is not None:
        for service in service_configs:
            if service.name == service_name:
                return [service]
    return []


@app.command()
async def init(
    directory: str = typer.Argument(None, help="Directory to initialize launchflow."),
    account_id: str = typer.Option(
        None,
        help="Account ID to use for this project. Defaults to the account ID set in the config.",
    ),
):
    """Initialize a new launchflow project."""
    async with async_launchflow_client_ctx() as client:
        try:
            project = await project_gen.project(client, account_id)

            if "aws" in project.configured_cloud_providers:
                cloud_provider = "aws"
            elif "gcp" in project.configured_cloud_providers:
                cloud_provider = "gcp"
            else:
                raise NotImplementedError(
                    f"Cloud provider {project.configured_cloud_providers} is not supported yet."
                )

            environment = await get_environment(
                client=client,
                project=project,
                environment_name=None,
                prompt_for_creation=True,
            )
        except Exception as e:
            typer.echo(e)
            raise typer.Exit(1)

        if not directory:
            relative_path = project.name
            full_directory_path = os.path.join(os.path.abspath("."), relative_path)
        else:
            relative_path = directory
            full_directory_path = os.path.abspath(relative_path)
        while os.path.exists(full_directory_path):
            typer.echo(f"Directory `{full_directory_path}` already exists.")
            directory_name = beaupy.prompt("Enter a directory name for your project:")
            full_directory_path = os.path.join(
                os.path.abspath(directory), directory_name
            )

        framework = project_gen.framework(cloud_provider)
        resources = project_gen.resources(cloud_provider)

        if framework == project_gen.Framework.FASTAPI:
            generator = FastAPIProjectGenerator(
                resources=resources,
                cloud_provider=cloud_provider,
                launchflow_project_name=project.name,
                launchflow_environment_name=environment.name,
            )
            generator.generate_project(full_directory_path)
        elif framework == project_gen.Framework.FLASK:
            generator = FlaskProjectGenerator(
                resources=resources,
                cloud_provider=cloud_provider,
                launchflow_project_name=project.name,
                launchflow_environment_name=environment.name,
            )
            generator.generate_project(full_directory_path)
        elif framework == project_gen.Framework.DJANGO:
            generator = DjangoProjectGenerator(
                resources=resources,
                cloud_provider=cloud_provider,
                launchflow_project_name=project.name,
                launchflow_environment_name=environment.name,
            )
            generator.generate_project(full_directory_path)
        else:
            raise NotImplementedError(f"Framework {framework} is not supported yet.")

        print()
        print("Done!")
        print()
        print("Navigate to your project directory:")
        rich.print(f"  $ [green]cd {relative_path}")
        print()
        print("To create your resources run:")
        rich.print("  $ [green]launchflow create")
        print()
        print("To build and deploy your app remotely run:")
        rich.print("  $ [green]launchflow deploy")


@app.command()
async def create(
    resource: str = typer.Argument(
        None,
        help="Resource to create. If none we will scan the directory for resources.",
    ),
    project: Optional[str] = typer.Option(None, help=PROJECT_HELP),
    environment: Optional[str] = typer.Option(None, help=ENVIRONMENT_HELP),
    scan_directory: str = typer.Option(".", help=SCAN_DIRECTORY_HELP),
    auto_approve: bool = typer.Option(
        False, "--auto-approve", "-y", help="Auto approve resource creation."
    ),
    api_key: Optional[str] = typer.Option(None, help=API_KEY_HELP),
):
    """Create any resources that are not already created."""
    try:
        async with async_launchflow_client_ctx(api_key=api_key) as client:
            project_info = await _get_project_info(client, project)
            environment_info = await _get_environment_info(
                client, project_info, environment
            )

            launchflow.project = project_info.name
            launchflow.environment = environment_info.name

            if resource is None:
                resources = find_launchflow_resources(scan_directory)
            else:
                resources = [resource]

            await create_resources(
                project_info.name,
                environment_info.name,
                *import_resources(resources),
                prompt=not auto_approve,
                api_key=api_key,
            )

    except LaunchFlowRequestFailure as e:
        e.pretty_print()
        raise typer.Exit(1)


@app.command()
async def clean(
    scan_directory: str = typer.Option(".", help=SCAN_DIRECTORY_HELP),
    project: Optional[str] = typer.Option(None, help=PROJECT_HELP),
    environment: Optional[str] = typer.Option(None, help=ENVIRONMENT_HELP),
):
    """Clean up any resources that are not in the current directory but are part of the project / environment."""
    try:
        async with async_launchflow_client_ctx() as client:
            project_info = await _get_project_info(client, project)
            environment_info = await _get_environment_info(
                client, project_info, environment
            )

            launchflow.project = project_info.name
            launchflow.environment = environment_info.name

            resources = find_launchflow_resources(scan_directory)
            await clean_resources(
                project_info.name,
                environment_info.name,
                *import_resources(resources),
            )

    except LaunchFlowRequestFailure as e:
        e.pretty_print()
        raise typer.Exit(1)


@app.command()
async def destroy(
    project: Optional[str] = typer.Option(None, help=PROJECT_HELP),
    environment: Optional[str] = typer.Option(None, help=ENVIRONMENT_HELP),
):
    """Destroy all resources in the project / environment."""
    try:
        async with async_launchflow_client_ctx() as client:
            project_info = await _get_project_info(client, project)
            environment_info = await _get_environment_info(
                client, project_info, environment
            )

            launchflow.project = project_info.name
            launchflow.environment = environment_info.name
            # NOTE: This prompts the user to confirm the destruction of each resource
            await destroy_resources(project_info.name, environment_info.name)

    except LaunchFlowRequestFailure as e:
        e.pretty_print()
        raise typer.Exit(1)


@app.command(hidden=True)
async def deploy(
    project: Optional[str] = typer.Option(None, help=PROJECT_HELP),
    environment: Optional[str] = typer.Option(None, help=ENVIRONMENT_HELP),
    service: Optional[str] = typer.Option(None, help=SERVICE_HELP),
    auto_approve: bool = typer.Option(
        False, "--auto-approve", "-y", help="Auto approve the deployment."
    ),
    api_key: Optional[str] = typer.Option(None, help=API_KEY_HELP),
    scan_directory: str = typer.Option(".", help=SCAN_DIRECTORY_HELP),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Verbose output. Will include all options provided to your service.",
    ),
):
    """Deploy a service to a project / environment."""
    async with async_launchflow_client_ctx(api_key=api_key) as client:
        try:
            project_info = await _get_project_info(client, project)
            environment_info = await _get_environment_info(
                client, project_info, environment
            )
            launchflow.project = project_info.name
            launchflow.environment = environment_info.name
            service_infos = _get_service_infos(service)
            services: List[Service] = []
            service_names = set()
            # Load services from config
            for service_info in service_infos:
                service_names.add(service_info.name)
                config = service_info.product_configs.get("base")
                env_config = service_info.product_configs.get(environment_info.name)
                if config is not None and env_config is not None:
                    config.merge(env_config)
                elif env_config is not None:
                    config = env_config
                if service_info.product == "gcp_cloud_run":
                    services.append(
                        CloudRun(
                            name=service_info.name,
                            dockerfile=service_info.dockerfile,
                            build_directory=service_info.build_directory,
                            build_ignore=service_info.build_ignore,
                            region=config.region if config else None,
                            cpu=config.cpu if config else None,
                            memory=config.memory if config else None,
                            port=config.port if config else None,
                            publicly_accessible=(
                                config.publicly_accessible if config else None
                            ),
                            min_instance_count=(
                                config.min_instance_count if config else None
                            ),
                            max_instance_count=(
                                config.max_instance_count if config else None
                            ),
                            max_instance_request_concurrency=(
                                config.max_instance_request_concurrency
                                if config
                                else None
                            ),
                            invokers=config.invokers if config else None,
                            custom_audiences=(
                                config.custom_audiences if config else None
                            ),
                            ingress=config.ingress if config else None,
                        )
                    )
                elif service_info.product == "aws_ecs_fargate":
                    services.append(
                        ECSFargate(
                            name=service_info.name,
                            dockerfile=service_info.dockerfile,
                            build_directory=service_info.build_directory,
                            build_ignore=service_info.build_ignore,
                        )
                    )
                else:
                    raise NotImplementedError(
                        f"Product {service_info.product} is not supported yet."
                    )
            # Load services from code
            found_services = import_services(find_launchflow_services(scan_directory))
            for found_service in found_services:
                if found_service.name in service_names:
                    typer.echo(
                        f"Service `{found_service.name}` is configured in launchflow.yaml and your code. Services may only be specified in code or in launchflow.yaml, not both."
                    )
                    raise typer.Exit(1)
                if service is not None and found_service.name != service:
                    continue
                services.append(found_service)
            if not services:
                typer.echo("No services found.")
                raise typer.Exit(1)
            await deploy_services(
                project_info.name,
                environment_info.name,
                *services,
                prompt=not auto_approve,
                api_key=api_key,
                verbose=verbose,
            )
        except LaunchFlowRequestFailure as e:
            e.pretty_print()
            raise typer.Exit(1)


@app.command()
async def login():
    """Login to LaunchFlow. If you haven't signup this will create a free account for you."""
    try:
        async with async_launchflow_client_ctx() as client:
            await login_flow(client)
    except Exception as e:
        typer.echo(f"Failed to login. {e}")
        typer.Exit(1)


@app.command()
def logout():
    """Logout of LaunchFlow."""
    try:
        logout_flow()
    except Exception as e:
        typer.echo(f"Failed to logout. {e}")
        typer.Exit(1)


@app.command()
async def connect(
    account_id: str = typer.Argument(
        None, help="The account ID to fetch. Of the format `acount_123`"
    ),
    provider: CloudProvider = typer.Option(
        None, help="The cloud provider to setup your account with."
    ),
    status: bool = typer.Option(
        False,
        "--status",
        "-s",
        help="Only print out connection status instead of instructions for connecting.",
    ),
):
    """Connect your LaunchFlow account to a cloud provider (AWS or GCP) or retrieve connection info with the `--status / -s` flag."""
    async with async_launchflow_client_ctx() as client:
        if status:
            account_id = await get_account_id_from_config(client, account_id)
            connection_status = await client.connect.status(account_id)
            to_print = connection_status.model_dump()
            del to_print["aws_connection_info"]["cloud_foundation_template_url"]
            print_response("Connection Status", to_print)
        else:
            try:
                await connect_provider(client, account_id, provider)
            except LaunchFlowRequestFailure as e:
                e.pretty_print()
                raise typer.Exit(1)
            except Exception as e:
                typer.echo(str(e))
                raise typer.Exit(1)


@app.command()
async def logs(
    operation_id: str = typer.Argument(
        None, help="The operation ID to fetch logs for."
    ),
):
    """Fetch the logs for a given operation."""
    async with async_launchflow_client_ctx() as client:
        try:
            operation = await client.operations.get(operation_id)
            if not operation.environment_name:
                typer.echo("Operation does not have an environment.")
                raise typer.Exit(1)
            environment = await client.environments.get(
                operation.project_name, operation.environment_name
            )
            if environment.aws_config:
                path = f"s3://{environment.aws_config.artifact_bucket}/logs/{operation_id}.log"
            elif environment.gcp_config:
                path = f"gs://{environment.gcp_config.artifact_bucket}/logs/{operation_id}.log"
            else:
                typer.echo("No artifact bucket found for environment.")
                raise typer.Exit(1)
            with fsspec.open(path) as f:
                print(f.read().decode("utf-8"))
        except LaunchFlowRequestFailure as e:
            e.pretty_print()
            raise typer.Exit(1)


# TODO: Would be nice to have environment be optional, but typer makes it difficult/messy
@app.command()
async def run(
    environment: str = typer.Argument(..., help=ENVIRONMENT_HELP),
    scan_directory: str = typer.Option(".", help=SCAN_DIRECTORY_HELP),
    args: Optional[List[str]] = typer.Argument(None, help="Additional command to run"),
):
    """Run a command against a remote environment OR local-enabled resources.

    Sample commands:

        launchflow run dev -- ./run.sh
            - Runs ./run.sh against dev environment resources.
        launchflow run local -- ./run.sh
            - Runs ./run.sh with local resources, using the environment from launchflow.yaml
              as a fallback for resources that aren't local enabled (e.g. anything in `launchflow.aws`
              or `launchflow.gcp`).
            - The environment MUST be specified in the launchflow.yaml if non-local resources are
              created in infra.py.
    """
    config_project = launchflow.project
    config_environment = launchflow.environment

    launchflow.config.local_mode = environment == "local"
    resources_refs = find_launchflow_resources(scan_directory)
    resources = import_resources(resources_refs)
    local_resources = [resource for resource in resources if is_local_resource(resource)]
    remote_resources = [resource for resource in resources if not is_local_resource(resource)]

    if environment == "local":
        if config_environment is None:
            if any(remote_resources):
                typer.echo("Tried to run in `local` mode with non-local resources in infra.py.")
                typer.echo("Please set one in launchflow.yaml.")
                raise typer.Exit(1)
        elif not remote_resources:
            typer.echo("Running with local generic resources.")
        else:
            typer.echo(f"Running with local generic resources, using {config_environment} as a fallback for resources:")
            for resource in remote_resources:
                typer.echo(f"  - {resource.name}\n")

    # TODO: Could change this to happen in one step and have the confirmation grouped together,
    #       but this requires a slight refactor of create_resources
    if local_resources:
        typer.echo("Creating local resources...")
        await create_resources("local", "local", *local_resources, prompt=False)
        typer.echo("Created local resources successfully.\n")

    if remote_resources:
        typer.echo("Creating remote resources...")
        remote_environment = config_environment if local_resources else environment
        await create_resources(config_project, remote_environment, *remote_resources, prompt=True)
        typer.echo("Created remote resources successfully.\n")

    if args is None:
        return

    console = Console()
    command = " ".join(args)
    os.environ["LAUNCHFLOW_LOCAL_MODE_ENABLED"] = str(launchflow.config.local_mode)
    proc = await asyncio.create_subprocess_shell(command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)

    try:
        stdout, stderr = await proc.communicate()

        stdout = stdout.decode() if stdout else ""
        stderr = stderr.decode() if stderr else ""
        output = stdout + stderr

        console.print(Panel(output, title="Program Output", expand=True))
    except asyncio.CancelledError:
        # TODO: I don't like this sleep but for some reason it starts before the above process has finished printing
        await asyncio.sleep(1)
        await stop_local_containers(prompt=False)
    finally:
        typer.echo("\nStopping running local resources...")
        await stop_local_containers(prompt=False)
        typer.echo("\nStopped local resources successfully.")

if __name__ == "__main__":
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    app()
