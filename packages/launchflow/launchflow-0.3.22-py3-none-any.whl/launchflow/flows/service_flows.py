import asyncio
import sys
from typing import List, Optional

import beaupy
import rich
import typer
from launchflow.cli.utils import import_from_string
from launchflow.operations import AsyncOp
from launchflow.service import Service
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Column

from launchflow.clients import async_launchflow_client_ctx


async def _monitor_deploy_service(
    progress: Progress,
    async_op: AsyncOp,
    service_name: str,
    api_key: Optional[str] = None,
):
    async with async_launchflow_client_ctx(api_key=api_key) as client:
        # TODO: List out the infra changes that will be made in the user's
        # account, like creating the docker repo, docker image, cloud run service, etc.

        # TODO: Add a way to notify the user of build progress

        # TODO: (maybe) add a ETA for the build
        description = f"Deploying [blue]{async_op.entity_ref}[/blue]..."
        deploy_task = progress.add_task(description, total=None)
        await async_op.run()
        last_message = ""
        async for (
            status,
            current_message,
        ) in client.operations.stream_operation_status_and_message(
            async_op.operation_id
        ):
            operation = await client.operations.get(async_op.operation_id)
            if status.is_error():
                progress.remove_task(deploy_task)
                progress.console.print(
                    f"[red]✗[/red] Deployment failed for [blue]{async_op.entity_ref}[/blue]"
                )
                progress.console.print(
                    f"    └── View logs for operation by running `launchflow logs {operation.id}`"
                )
                if operation.build_url:
                    progress.console.print(
                        f"    └── View build logs at {operation.build_url}"
                    )
                return False
            elif status.is_cancelled():
                progress.remove_task(deploy_task)
                progress.console.print(
                    f"[yellow]✗[/yellow] Deployment cancelled for [blue]{async_op.entity_ref}[/blue]"
                )
                return False
            elif status.is_success():
                service = await client.services.get(
                    project_name=operation.project_name,
                    environment_name=operation.environment_name,
                    service_name=service_name,
                )
                progress.remove_task(deploy_task)
                progress.console.print(
                    f"[green]✓[/green] Deployment successful for [blue]{async_op.entity_ref}[/blue]"
                )
                if service.service_url:
                    progress.console.print(
                        f"    └── View service at {service.service_url}"
                    )
                return True
            elif last_message != current_message:
                last_message = current_message
                new_description = f"{description}\n    └── {current_message}"
                description = new_description
                progress.update(deploy_task, description=description)


def import_services(service_import_strs: List[str]) -> List[Service]:
    sys.path.insert(0, "")
    services: List[Service] = []
    for service_str in service_import_strs:
        imported_service = import_from_string(service_str)
        if not isinstance(imported_service, Service):
            raise ValueError(f"Service {imported_service} is not a valid Service")
        services.append(imported_service)
    return services


async def deploy(
    project: str,
    environment: str,
    *services: Service,
    prompt: bool = True,
    api_key: Optional[str] = None,
    verbose: bool = False,
):
    if not prompt:
        selected_services = services
    else:
        selected_services: List[Service] = []
        if len(services) == 1:
            selected_service = services[0]
            if verbose:
                service_ref = str(selected_service)
            else:
                service_ref = (
                    f"{selected_service.__class__.__name__}({selected_service.name})"
                )
            service_ref = str(selected_service)

            answer = beaupy.confirm(
                f"[bold]Deploy[/bold] [blue]{service_ref}[/blue] to [bold yellow]`{project}/{environment}`[/bold yellow]?"
            )
            if not answer:
                print("User cancelled deployment. Exiting.")
                return
            selected_services.append(selected_service)
        else:
            rich.print(
                f"Select the services you want to deploy to [bold yellow]`{project}/{environment}`[/bold yellow]."
            )
            service_refs = []
            for selected_service in services:
                if verbose:
                    service_ref = str(selected_service)
                else:
                    service_ref = f"{selected_service.__class__.__name__}({selected_service.name})"
                service_refs.append(service_ref)
            selected = beaupy.select_multiple(service_refs, return_indices=True)
            for answer in selected:
                rich.print(f"[pink1]>[/pink1] {service_refs[answer]}")
                selected_services.append(services[answer])
    if not selected_services:
        print("No services selected. Exiting.")
        return
    coros = []
    with Progress(
        SpinnerColumn(),
        # NOTE: we provide column here to customize how overflow is displayed since the build urls can be kind of long
        TextColumn(
            "[progress.description]{task.description}",
            table_column=Column(no_wrap=False, overflow="fold"),
        ),
    ) as progress:
        for to_deploy in selected_services:
            coros.append(
                _monitor_deploy_service(
                    progress,
                    await to_deploy.deploy_async(
                        project_name=project,
                        environment_name=environment,
                        api_key=api_key,
                    ),
                    service_name=to_deploy.name,
                    api_key=api_key,
                )
            )
        results = await asyncio.gather(*coros)
        if not all(results):
            raise typer.Exit(1)
