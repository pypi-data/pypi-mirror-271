import asyncio
import dataclasses
import logging
import sys
from typing import List, Optional, Tuple, Union

import beaupy
import deepdiff
import rich
from docker.models.containers import Container
from launchflow.cli.utils import import_from_string
from launchflow.clients.docker_client import DockerClient, docker_service_available
from launchflow.clients.response_schemas import (
    OperationResponse,
    OperationStatus,
    ResourceResponse,
    ServiceResponse,
)
from launchflow.context import docker_ctx
from launchflow.docker.resource import DockerResource
from launchflow.exceptions import LaunchFlowRequestFailure
from launchflow.operations import AsyncOp, AsyncResourceNoOp, AsyncResourcePendingOp
from launchflow.postgres import GenericResource
from launchflow.resource import Resource
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

import launchflow
from launchflow.clients import LaunchFlowAsyncClient, async_launchflow_client_ctx


@dataclasses.dataclass
class ContainerResource:
    container: Container

    def __str__(self):
        return f'DockerContainer(name="{self.container.name}", image="{self.container.image.tags[0]}")'

    def __hash__(self) -> int:
        return hash(self.container.name)


def compare_dicts(d1, d2):
    return "\n        ".join(
        deepdiff.DeepDiff(d1, d2)
        .pretty()
        # NOTE: we replace these so rich doesn't get upset
        .replace("[", "{")
        .replace("]", "}")
        .replace("root", "")
        .split("\n")
    )


async def _monitor_delete_resource_operations(
    async_launchflow_client: LaunchFlowAsyncClient,
    project: str,
    environment: str,
    resources_to_delete: List[ResourceResponse],
    services_to_delete: List[ServiceResponse],
    containers_to_delete: List[ContainerResource],
):
    # Add a new line here to make output a little cleaner
    print()
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        TextColumn("["),
        TimeElapsedColumn(),
        TextColumn("]"),
    ) as progress:
        operations: List[Tuple[OperationResponse, int]] = []
        task_to_resource = {}
        for resource in resources_to_delete:
            task = progress.add_task(f"Deleting [blue]{resource}[/blue]...", total=1)
            task_to_resource[task] = resource
            name = resource.name.split("/")[-1]
            operations.append(
                (
                    await async_launchflow_client.resources.delete(
                        project_name=project,
                        environment_name=environment,
                        resource_name=name,
                    ),
                    task,
                )
            )
        # TODO: better separate Resource / Service / Container deletion
        for service in services_to_delete:
            task = progress.add_task(f"Deleting [blue]{service}[/blue]...", total=1)
            task_to_resource[task] = service
            name = service.name.split("/")[-1]
            operations.append(
                (
                    await async_launchflow_client.services.delete(
                        project_name=project,
                        environment_name=environment,
                        service_name=name,
                    ),
                    task,
                )
            )
        docker_client = None
        docker_containers: List[Tuple[Container, int]] = []
        for container in containers_to_delete:
            if docker_client is None:
                docker_client = DockerClient()
            task = progress.add_task(f"Deleting [blue]{container}[/blue]...", total=1)
            task_to_resource[task] = container
            docker_client.stop_container(container.container.name)
            docker_containers.append((container.container, task))

        successes = 0
        failures = 0
        while operations or docker_containers:
            await asyncio.sleep(3)
            to_stream_operations = []
            to_stream_containers = []
            for operation, task in operations:
                try:
                    status = (
                        await async_launchflow_client.operations.get_operation_status(
                            operation_id=operation.id
                        )
                    )
                except LaunchFlowRequestFailure as e:
                    if e.status_code == 404:
                        status = OperationStatus.SUCCESS
                    else:
                        raise e
                if status.is_final():
                    progress.remove_task(task)
                    resource = task_to_resource[task]
                    success = await _print_operation_status_v2(
                        progress=progress,
                        status=status,
                        success_message=None,
                        entity_ref=str(resource),
                        operation_id=operation.id,
                        operation_type="Deletion",
                    )
                    if success:
                        successes += 1
                    else:
                        failures += 1
                else:
                    to_stream_operations.append((operation, task))

            for container, task in docker_containers:
                try:
                    container.reload()
                    if container.status == "exited":
                        docker_client.remove_container(container.name)
                        docker_ctx.remove_resource_directory(container.name)
                        progress.remove_task(task)
                        resource = task_to_resource[task]
                        progress.console.print(
                            f"[green]✓[/green] Deletion successful for [blue]{resource}[/blue]"
                        )
                        successes += 1
                    else:
                        to_stream_containers.append((container, task))
                except Exception as e:
                    progress.remove_task(task)
                    resource = task_to_resource[task]
                    progress.console.print(f"[red]✗[/red] Failed to delete {resource}")
                    progress.console.print(f"    └── {e}")
                    failures += 1

            operations = to_stream_operations
            docker_containers = to_stream_containers
        if successes:
            progress.console.print(
                f"[green]✓[/green] Successfully deleted {successes} resources"
            )
        if failures:
            progress.console.print(
                f"[red]✗[/red] Failed to delete {failures} resources"
            )


async def _print_operation_status_v2(
    progress: Progress,
    status: Optional[OperationStatus],
    success_message: Optional[str],
    operation_id: str,
    entity_ref: str,
    operation_type: str,
):
    if status is None:
        progress.console.print(
            f"[yellow]✗[/yellow] {operation_type} status unknown for [blue]{entity_ref}[/blue]"
        )
    elif status.is_success():
        progress.console.print(
            f"[green]✓[/green] {operation_type} successful for [blue]{entity_ref}[/blue]"
        )
        if success_message:
            progress.console.print(f"    └── {success_message}")
        return True
    elif status.is_error():
        progress.console.print(
            f"[red]✗[/red] {operation_type} failed for [blue]{entity_ref}[/blue]"
        )
        progress.console.print(
            f"    └── View logs for operation by running `launchflow logs {operation_id}`"
        )
        progress.console.print("")
    elif status.is_cancelled():
        progress.console.print(
            f"[yellow]✗[/yellow] {operation_type} cancelled for [blue]{entity_ref}[/blue]"
        )
    else:
        progress.console.print(
            f"[yellow]?[/yellow] {operation_type} status unknown for [blue]{entity_ref}[/blue]"
        )
    return False


async def _run_and_monitor_resource_operations(resource_ops: List[AsyncOp]):
    # Add a new line here to make output a little cleaner
    print()
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        TextColumn("["),
        TimeElapsedColumn(),
        TextColumn("]"),
    ) as progress:
        started_operations: List[Tuple[AsyncOp, int]] = []
        for resource_op in resource_ops:
            if resource_op._type == "create":
                op_type = "Creating"
            elif resource_op._type == "replace":
                op_type = "Replacing"
            else:
                raise ValueError(f"Unknown operation type {resource_op._type}")
            task = progress.add_task(
                f"{op_type} [blue]{resource_op.entity_ref}[/blue]...", total=1
            )
            started_operations.append((resource_op, task))

        # NOTE: This is what actually starts the operations
        results = await asyncio.gather(
            *[op.run() for op in resource_ops], return_exceptions=True
        )
        operations: List[Tuple[AsyncOp, int]] = []
        for result, (resource_op, task) in zip(results, started_operations):
            if isinstance(result, Exception):
                progress.remove_task(task)
                progress.console.print(
                    f"[red]✗[/red] Failed to start operation for [blue]{resource_op.entity_ref}[/blue]"
                )
                progress.console.print(f"    └── {result}")
            else:
                operations.append((resource_op, task))

        create_successes = 0
        create_failures = 0
        replace_successes = 0
        replace_failures = 0
        while operations:
            await asyncio.sleep(3)
            to_stream_operations = []
            for operation, task in operations:
                status = await operation.get_status()
                if status.is_final():
                    progress.remove_task(task)
                    success = await _print_operation_status_v2(
                        progress=progress,
                        status=status,
                        success_message=operation.success_message,
                        operation_id=operation.operation_id,
                        entity_ref=operation.entity_ref,
                        operation_type=(
                            "Creation" if operation._type == "create" else "Replacement"
                        ),
                    )
                    if success:
                        if operation._type == "replace":
                            replace_successes += 1
                        else:
                            create_successes += 1
                    else:
                        if operation._type == "replace":
                            replace_failures += 1
                        else:
                            create_failures += 1
                else:
                    to_stream_operations.append((operation, task))
            operations = to_stream_operations
        if create_successes:
            progress.console.print(
                f"[green]✓[/green] Successfully created {create_successes} resources"
            )
        if replace_successes:
            progress.console.print(
                f"[green]✓[/green] Successfully replaced {replace_successes} resources"
            )
        if create_failures:
            progress.console.print(
                f"[red]✗[/red] Failed to create {create_failures} resources"
            )
        if replace_failures:
            progress.console.print(
                f"[red]✗[/red] Failed to replace {replace_failures} resources"
            )


def import_resources(resource_import_strs: List[str]) -> List[Resource]:
    sys.path.insert(0, "")
    resources: List[Resource] = []
    for resource_str in resource_import_strs:
        imported_resource = import_from_string(resource_str)
        if not isinstance(imported_resource, Resource) and not isinstance(
            imported_resource, GenericResource
        ):
            continue
        resources.append(imported_resource)
    return resources


def is_local_resource(resource: Resource) -> bool:
    if isinstance(resource, DockerResource) and not launchflow.config.local_mode:
        logging.warning(
            "Docker resource %s is a local resource, but launchflow isn't running in local mode"
            % resource
        )

    if not launchflow.config.local_mode:
        return False

    return isinstance(resource, DockerResource) or isinstance(resource, GenericResource)


async def create(
    project: str,
    environment: str,
    *resources: Resource,
    prompt: bool = True,
    api_key: Optional[str] = None,
):
    # 1. Check which resources exist and whicn don't
    # TODO: do this async or maybe add a batch get endpoint
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
    ) as progress:
        task = progress.add_task(
            f"Loading application for: [bold yellow]`{project}/{environment}`[/bold yellow]",
        )
        all_resource_ops = []

        for resource in resources:
            all_resource_ops.append(
                resource.create_async(
                    replace=True,
                    project_name=project,
                    environment_name=environment,
                    api_key=api_key,
                )
            )

        all_resource_ops: List[
            Union[AsyncOp, AsyncResourceNoOp]
        ] = await asyncio.gather(*all_resource_ops)

        create_ops: List[AsyncOp] = []
        replace_ops: List[AsyncOp] = []
        no_ops: List[AsyncResourceNoOp] = []
        pending_ops: List[AsyncResourcePendingOp] = []
        for op in all_resource_ops:
            if op._type == "create":
                create_ops.append(op)
            elif op._type == "replace":
                replace_ops.append(op)
            elif op._type == "noop":
                no_ops.append(op)
                progress.console.print(
                    f"[green]✓[/green] [blue]{op.entity_ref}[/blue] already exists"
                )
            elif op._type == "pending":
                no_ops.append(op)
                # TODO make consistent whether or not there's a period at the end of lines
                progress.console.print(
                    f"[red]✗[/red] [blue]{op.entity_ref}[/blue] is in a pending state."
                )
            else:
                raise ValueError(f"Unknown operation type {op._type}")

        progress.remove_task(task)

    # 2. Prompt the user for what should be created
    to_run = []
    if not create_ops and not replace_ops:
        if pending_ops:
            progress.console.print(
                "[red]✗[/red] Encountered resources in pending states, please wait for them to finish and try again"
            )
        else:
            progress.console.print(
                "[green]✓[/green] All resources already exist. No action required."
            )
        return
    if prompt:
        options = []
        all_resources = []
        for op in create_ops:
            options.append(f"[bold]Create[/bold]: [blue]{op.entity_ref}[/blue]")
            all_resources.append((op, False))
        for op in replace_ops:
            options.append(
                f"[bold]Replace[/bold]: [blue]{op.entity_ref}[/blue]\n"
                f"    └── {compare_dicts(op._create_args, op._replace_args)}"
            )
            all_resources.append((op, True))
        rich.print(
            f"Select the resource operations you would like to perform in [bold yellow]`{project}/{environment}`[/bold yellow]:"
        )
        answers = beaupy.select_multiple(
            options, return_indices=True, ticked_indices=list(range(len(options)))
        )
        for answer in answers:
            op, replace = all_resources[answer]
            rich.print(f"[pink1]>[/pink1] {options[answer]}")
            to_run.append(op)
        if not to_run:
            progress.console.print(
                "[green]✓[/green] No resources selected. No action required."
            )
            return
    else:
        for op in create_ops:
            to_run.append(op)
        for op in replace_ops:
            to_run.append(op)

    # 3. Create the resources
    await _run_and_monitor_resource_operations(to_run)


async def clean(
    project: str,
    environment: str,
    *local_resources: Resource,
    prompt: bool = True,
):
    async with async_launchflow_client_ctx() as async_launchflow_client:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
        ) as progress:
            task = progress.add_task(
                f"Loading application for: [bold yellow]`{project}/{environment}`[/bold yellow]",
            )
            keyed_local_resources = {}
            for local_resource in local_resources:
                name = f"{project}/{environment}/{local_resource.name}"
                keyed_local_resources[name] = local_resource
            remote_resources = await async_launchflow_client.resources.list(
                project_name=project,
                environment_name=environment,
            )

            to_delete_options = []
            for remote_resource in remote_resources:
                if (
                    remote_resource.name not in keyed_local_resources
                    and remote_resource.status in ["ready", "failed"]
                ):
                    to_delete_options.append(remote_resource)
            progress.remove_task(task)
        to_delete = []
        if not to_delete_options:
            progress.console.print(
                "[green]✓[/green] No resources to delete. No action required."
            )
            return
        if prompt:
            rich.print(
                f"The following resources were unused in [bold yellow]`{project}/{environment}`[/bold yellow]. Select the resources you would like to [bold]delete[/bold]:"
            )
            options = [
                f"[bold]Delete[/bold]: [bold]{str(resource)}[/bold]"
                for resource in to_delete_options
            ]
            answers = beaupy.select_multiple(options, return_indices=True)
            for answer in answers:
                rich.print(
                    f"[pink1]>[/pink1] Delete: [blue]{to_delete_options[answer]}[/blue]"
                )
                to_delete.append(to_delete_options[answer])
            if not to_delete:
                rich.print(
                    "[green]✓[/green] No resources selected. No action required."
                )
                return
        else:
            to_delete = to_delete_options
        await _monitor_delete_resource_operations(
            async_launchflow_client, project, environment, to_delete, [], []
        )


# This is the same as clean, but deletes all resources instead of just the ones that are unused
async def destroy(
    project: str,
    environment: str,
    prompt: bool = True,
):
    async with async_launchflow_client_ctx() as async_launchflow_client:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
        ) as progress:
            task = progress.add_task(
                f"Loading resources for: [bold yellow]`{project}/{environment}`[/bold yellow]",
            )
            remote_resources = await async_launchflow_client.resources.list(
                project_name=project,
                environment_name=environment,
            )
            remote_services = await async_launchflow_client.services.list(
                project_name=project,
                environment_name=environment,
            )
            local_containers = []
            if docker_service_available():
                local_containers = [
                    ContainerResource(container)
                    for container in DockerClient().list_containers()
                ]
            to_delete_options = []
            for remote_resource in remote_resources:
                if remote_resource.status in ["ready", "failed"]:
                    to_delete_options.append((remote_resource, "resource"))
            for remote_service in remote_services:
                if remote_service.status in ["ready", "failed"]:
                    to_delete_options.append((remote_service, "service"))
            for container in local_containers:
                if container.container.status == "running":
                    to_delete_options.append((container, "container"))

            progress.remove_task(task)
        resources_to_delete = []
        services_to_delete = []
        containers_to_delete = []
        if not to_delete_options:
            progress.console.print(
                "[green]✓[/green] No resources to delete. No action required."
            )
            return
        if prompt:
            rich.print(
                f"The following items were found in [bold yellow]`{project}/{environment}`[/bold yellow]. Select what you would like to [bold]delete[/bold]:"
            )
            options = [
                f"[bold]Delete[/bold]: [bold]{str(resource)}[/bold]"
                for (resource, _) in to_delete_options
            ]
            answers = beaupy.select_multiple(options, return_indices=True)
            for answer in answers:
                rich.print(
                    f"[pink1]>[/pink1] Delete: [blue]{to_delete_options[answer][0]}[/blue]"
                )
                if to_delete_options[answer][1] == "resource":
                    resources_to_delete.append(to_delete_options[answer][0])
                elif to_delete_options[answer][1] == "service":
                    services_to_delete.append(to_delete_options[answer][0])
                else:
                    containers_to_delete.append(to_delete_options[answer][0])
            if (
                not resources_to_delete
                and not services_to_delete
                and not containers_to_delete
            ):
                rich.print(
                    "[green]✓[/green] No resources selected. No action required."
                )
                return
        else:
            for resource, resource_type in to_delete_options:
                if resource_type == "resource":
                    resources_to_delete.append(resource)
                elif resource_type == "service":
                    services_to_delete.append(resource)
                else:
                    containers_to_delete.append(resource)
        await _monitor_delete_resource_operations(
            async_launchflow_client,
            project,
            environment,
            resources_to_delete,
            services_to_delete,
            containers_to_delete,
        )


async def stop_local_containers(
    prompt: bool = True,
):
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
    ) as progress:
        task = progress.add_task(
            "Loading local resource",
        )
        containers = []
        if docker_service_available():
            containers = [
                ContainerResource(container)
                for container in DockerClient().list_containers()
            ]
        to_stop_options = [
            container
            for container in containers
            if container.container.status == "running"
        ]
        progress.remove_task(task)

    to_stop = set()
    if not to_stop_options:
        progress.console.print(
            "[green]✓[/green] No containers to stop. No action required."
        )
        return
    if prompt:
        rich.print(
            "The following running local containers were found. Select which you would like to [bold]stop[/bold]:"
        )
        options = [
            f"[bold]Stop[/bold]: [bold]{container}[/bold]"
            for container in to_stop_options
        ]
        answers = beaupy.select_multiple(options, return_indices=True)
        for answer in answers:
            rich.print(f"[pink1]>[/pink1] Stop: [blue]{to_stop_options[answer]}[/blue]")
            to_stop.add(to_stop_options[answer])
        if not to_stop:
            rich.print("[green]✓[/green] No containers selected. No action required.")
            return
    else:
        for container in to_stop_options:
            to_stop.add(container)

    docker_client = None
    stop_queue = set()
    for container in to_stop:
        task = progress.add_task(f"Stopping [blue]{container}[/blue]...", total=1)

        if docker_client is None:
            docker_client = DockerClient()
        docker_client.stop_container(container.container.name)

        stop_queue.add((container, task))

    successes = 0
    failures = 0
    while stop_queue:
        await asyncio.sleep(0.5)

        while stop_queue:
            container, task = stop_queue.pop()
            try:
                container.container.reload()
                if container.container.status == "exited":
                    progress.console.print(
                        f"[green]✓[/green] Stop successful for [blue]{container}[/blue]"
                    )
                    successes += 1
            except Exception as e:
                progress.remove_task(task)
                progress.console.print(f"[red]✗[/red] Failed to stop {container}")
                progress.console.print(f"    └── {e}")
                failures += 1
            finally:
                progress.remove_task(task)

    if successes:
        progress.console.print(
            f"[green]✓[/green] Successfully stopped {successes} containers"
        )
    if failures:
        progress.console.print(f"[red]✗[/red] Failed to stop {failures} containers")
