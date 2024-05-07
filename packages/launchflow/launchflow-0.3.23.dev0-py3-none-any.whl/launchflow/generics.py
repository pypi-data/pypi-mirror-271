from abc import ABC, abstractmethod
from typing import Literal, Optional

from httpx import Client, Timeout
from launchflow.aws.elasticache import ElasticacheRedis
from launchflow.aws.rds import RDSPostgres
from launchflow.clients.projects_client import ProjectsSyncClient
from launchflow.docker import DockerPostgres, DockerRedis
from launchflow.gcp.cloudsql import CloudSQLPostgres
from launchflow.gcp.memorystore import MemorystoreRedis
from launchflow.generic_clients import PostgresClient, RedisClient

import launchflow


class GenericResource(ABC):

    def __init__(self, name: str):
        self.name = name

        if launchflow.config.local_mode:
            cloud_provider = "local"
        elif (config_provider := launchflow.config.env.cloud_provider) is not None:
            cloud_provider = config_provider
        else:
            # TODO: Move this behind the launchflow context
            with Client(timeout=Timeout(30)) as http_client:
                projects_client = ProjectsSyncClient(http_client)
                remote_project = projects_client.get(launchflow.project)
                if len(remote_project.configured_cloud_providers) > 1:
                    raise ValueError("Multiple cloud providers are not supported")
                elif not remote_project.configured_cloud_providers:
                    raise ValueError(
                        f"No cloud provider is configured for project: {launchflow.project}"
                    )
                else:
                    cloud_provider = remote_project.configured_cloud_providers[0]
        self._initialize_strategy(cloud_provider)

        if not hasattr(self, "_strategy") or self._strategy is None:
            raise ValueError("Generic was initialized without a underlying strategy.")

    @property
    def product_name(self) -> str:
        return self._strategy.product_name

    @abstractmethod
    def _initialize_strategy(self, cloud_provider: Literal["gcp", "aws", "local"]):
        raise NotImplementedError

    def connect(self):
        return self._strategy.connect()

    async def connect_async(self):
        return await self._strategy.connect_async()

    def create(
        self,
        *,
        project_name: Optional[str] = None,
        environment_name: Optional[str] = None,
        replace: bool = False,
    ):
        return self._strategy.create(
            project_name=project_name,
            environment_name=environment_name,
            replace=replace,
        )

    async def create_async(
        self,
        *,
        project_name: Optional[str] = None,
        environment_name: Optional[str] = None,
        replace: bool = False,
        api_key: Optional[str] = None,
    ):
        return await self._strategy.create_async(
            project_name=project_name,
            environment_name=environment_name,
            replace=replace,
            api_key=api_key,
        )


class Postgres(GenericResource, PostgresClient):

    def _initialize_strategy(self, cloud_provider: Literal["gcp", "aws", "local"]):
        if cloud_provider == "gcp":
            self._strategy = CloudSQLPostgres(self.name)
        elif cloud_provider == "aws":
            self._strategy = RDSPostgres(self.name)
        elif cloud_provider == "local":
            self._strategy = DockerPostgres(self.name)
        else:
            raise ValueError("Invalid cloud provider: ", cloud_provider)

    def django_settings(self, *args, **kwargs):
        return self._strategy.django_settings(*args, **kwargs)

    def sqlalchemy_engine_options(self, *args, **kwargs):
        return self._strategy.sqlalchemy_engine_options(*args, **kwargs)

    async def sqlalchemy_async_engine_options(self, *args, **kwargs):
        return await self._strategy.sqlalchemy_async_engine_options(*args, **kwargs)

    def sqlalchemy_engine(self, *args, **kwargs):
        return self._strategy.sqlalchemy_engine(*args, **kwargs)

    async def sqlalchemy_async_engine(self, *args, **kwargs):
        return await self._strategy.sqlalchemy_async_engine(*args, **kwargs)


class Redis(GenericResource, RedisClient):

    def _initialize_strategy(self, cloud_provider: Literal["gcp", "aws", "local"]):
        if cloud_provider == "gcp":
            self._strategy = MemorystoreRedis(self.name)
        elif cloud_provider == "aws":
            self._strategy = ElasticacheRedis(self.name)
        elif cloud_provider == "local":
            self._strategy = DockerRedis(self.name)
        else:
            raise ValueError("Invalid cloud provider: ", cloud_provider)

    def django_settings(self, *args, **kwargs):
        return self._strategy.django_settings(*args, **kwargs)

    def redis(self, *args, **kwargs):
        return self._strategy.redis(*args, **kwargs)

    async def redis_async(self, *args, **kwargs):
        return await self._strategy.redis_async(*args, **kwargs)
