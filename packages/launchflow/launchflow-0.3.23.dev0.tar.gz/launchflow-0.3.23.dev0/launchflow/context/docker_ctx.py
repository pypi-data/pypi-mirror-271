import logging
import os
import random
import shutil
import socket
from dataclasses import dataclass
from typing import Any, Dict, Optional

import yaml
from docker.models.containers import Container
from launchflow.clients.docker_client import (
    DockerClient,
    PortAlreadyAllocatedError,
    hash_create_args,
)
from launchflow.config.launchflow_yaml import find_launchflow_yaml
from launchflow.operations import AsyncDockerResourceNoOp, AsyncDockerResourceOp
from pydantic import BaseModel

from launchflow import exceptions

MAX_ASSIGNABLE_PORT = 65535


def find_open_port(start_port: int = 5432, max_checks = 20) -> int:
    """Find an open port starting from a given port.

    Chooses a port randomly from a range to make retries easy -- if two resources try to use
    the same port and collide, they have a tiny probability of colliding again the next time.

    Args:
    - `start_port`: The port to start searching from.
    - `max_checks`: The number of ports to check before giving up.

    Returns:
    - The port number found.
    """
    search_range = (start_port, MAX_ASSIGNABLE_PORT)
    for _ in range(max_checks):
        port = random.randint(*search_range)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("", port))
                return port
            except OSError:
                continue

    raise RuntimeError(f"Could not find an open port in range {search_range} after {max_checks} checks.")


@dataclass
class DockerContext:
    _docker_client: DockerClient = None


    # TODO update resource type after fixing circular import issue
    def _start_container_with_retries(self, resource: Any, volumes: Dict[str, Dict[str, str]], max_retries: int = 1) -> Optional[Container]:
        logging.info(f"Starting new container '{resource.name}'")

        remaining_retries = max_retries + 1
        container = None

        while remaining_retries > 0:
            try:
                container = self.docker_client.start_container(
                    name=resource.name,
                    image=resource._docker_image,
                    env_vars=resource._env_vars,
                    command=resource._command,
                    ports=resource._ports,
                    volumes=volumes,
                )
                break
            except PortAlreadyAllocatedError:
                remaining_retries -= 1
                logging.warning("Reassigning the ports due to a port allocated error and retrying!")
                resource.refresh_ports()
                self.docker_client.remove_container(resource.name)

        return container

    @property
    def docker_client(self):
        if self._docker_client is None:
            self._docker_client = DockerClient()
        return self._docker_client

    def get_resource_connection_info_sync(
        self,
        image_name: str,
        resource_name: str,
    ) -> Dict:
        # TODO: add a check to see if the resource's image_name matches the provided one
        del image_name
        # Load connection info from local .launchflow directory
        launchflow_yaml_path = find_launchflow_yaml()
        dot_launchflow_path = os.path.join(
            os.path.dirname(launchflow_yaml_path), ".launchflow"
        )
        resource_connection_info_path = os.path.join(
            dot_launchflow_path, "resources", resource_name, "connection_info.yaml"
        )
        if not os.path.exists(resource_connection_info_path):
            raise exceptions.ConnectionInfoNotFound(resource_name)

        try:
            with open(resource_connection_info_path, mode="r") as file:
                resource_connection_info = yaml.safe_load(file.read())
        except FileNotFoundError:
            raise exceptions.ConnectionInfoNotFound(resource_name)

        return resource_connection_info

    # TODO Refactor this to only take in the resource
    def create_resource_operation_sync(
        self,
        resource: Any,  # DockerResource, TODO resolve circular import so the type can be imported
        resource_type: str,
        image_name: str,
        resource_name: str,
        env_vars: Dict,
        ports: Dict,
        connection_info: BaseModel,
        replace: bool = False,
    ):
        launchflow_yaml_path = find_launchflow_yaml()
        dot_launchflow_path = os.path.join(
            os.path.dirname(launchflow_yaml_path), ".launchflow"
        )
        resource_connection_info_path = os.path.join(
            dot_launchflow_path, "resources", resource_name, "connection_info.yaml"
        )
        resource_volume_path = os.path.join(
            dot_launchflow_path, "resources", resource_name, "volume"
        )
        os.makedirs(resource_volume_path, exist_ok=True)

        # TODO: add support for individual resources to set more than just home
        # (e.g. /var/lib/postgresql/data)
        volumes = {resource_volume_path: {"bind": "/home", "mode": "rw"}}

        create_args = {
            "name": resource_name,
            "image": image_name,
            "env_vars": env_vars,
            "command": resource._command,
            "ports": ports,
            "volumes": volumes,
        }

        existing_container = self.docker_client.get_container(resource_name)
        if (
            existing_container is not None
            and existing_container.status == "running"
            and hash_create_args(create_args) == existing_container.labels.get("create_args_hash", None)
        ):
            logging.debug(
                f"Resource '{resource_name}' already exists with the same create args"
            )
            return AsyncDockerResourceNoOp(
                entity_ref=f"{resource_type}(name={resource_name})",
                container=None,
                _op=None,
            )
        elif existing_container is not None:
            if not replace:
                raise exceptions.ResourceReplacementRequired(resource_name)

            async def replace_operation():
                logging.info(
                    f"Stopping and removing existing container '{resource_name}'"
                )
                self.docker_client.stop_container(resource_name)
                self.docker_client.remove_container(resource.name)
                container = self._start_container_with_retries(resource, volumes)

                logging.info(f"Container '{resource_name}' started successfully.")
                logging.info(
                    f"Writing connection info to '{resource_connection_info_path}'"
                )

                with open(resource_connection_info_path, mode="w") as file:
                    file.write(yaml.dump(resource.connection_info().model_dump(mode="json")))
                return container

            return AsyncDockerResourceOp(
                entity_ref=f"{resource_type}(name={resource_name})",
                container=None,
                _op=replace_operation,
                _type="replace",
                _create_args=create_args,
            )
        else:

            async def create_operation():
                logging.info(f"Starting new container '{resource_name}'")
                container = self._start_container_with_retries(resource, volumes)

                logging.info(f"Container '{resource_name}' started successfully.")
                logging.info(
                    f"Writing connection info to '{resource_connection_info_path}'"
                )
                with open(resource_connection_info_path, mode="w") as file:
                    file.write(yaml.dump(connection_info.model_dump(mode="json")))
                return container

            return AsyncDockerResourceOp(
                entity_ref=f"{resource_type}(name={resource_name})",
                container=None,
                _op=create_operation,
                _type="create",
                _create_args=create_args,
            )

    # TODO: Consider moving all destroy logic into this DockerContext class instead of
    # having the resource destroy flow handle it (this method is called by the flow)
    def remove_resource_directory(self, resource_name: str):
        launchflow_yaml_path = find_launchflow_yaml()
        dot_launchflow_path = os.path.join(
            os.path.dirname(launchflow_yaml_path), ".launchflow"
        )
        resource_path = os.path.join(dot_launchflow_path, "resources", resource_name)
        if not os.path.exists(resource_path):
            logging.warning(f"Resource directory '{resource_path}' does not exist.")
            return
        logging.info(f"Removing resource directory '{resource_path}'")
        shutil.rmtree(resource_path)
        logging.info(f"Resource directory '{resource_path}' removed successfully.")
