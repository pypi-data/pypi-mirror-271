# Handling imports and missing dependencies
try:
    import redis
except ImportError:
    redis = None

from launchflow.context.docker_ctx import find_open_port
from launchflow.docker.resource import DockerResource
from pydantic import BaseModel


def _check_redis_installs():
    if redis is None:
        raise ImportError(
            "redis library is not installed. Please install it with `pip install redis`."
        )


class DockerRedisConnectionInfo(BaseModel):
    password: str
    redis_port: str


class DockerRedis(DockerResource[DockerRedisConnectionInfo]):

    def __init__(self, name: str, *, password: str = "password") -> None:
        """A Redis resource running in a Docker container.

        **Args**:
        - `name` (str): The name of the Redis docker resource. This must be globally unique.
        - `password` (str): The password for the Redis DB. If not provided, a standard password will be used.

        **Example usage:**
        ```python
        import launchflow as lf

        redis = lf.DockerRedis("my-redis-instance")

        # Set a key-value pair
        client = redis.redis()
        client.set("my-key", "my-value")

        # Async compatible
        async_client = await redis.redis_async()
        await async_client.set("my-key", "my-value")
        ```
        """
        self.password = password
        redis_port = find_open_port()

        super().__init__(
            name=name,
            env_vars={},
            command=f"redis-server --appendonly yes --requirepass {password}",
            ports={"6379/tcp": redis_port},
            docker_image="redis",
        )

        self._sync_client = None
        self._async_pool = None

    def connection_info(self) -> DockerRedisConnectionInfo:
        return DockerRedisConnectionInfo(
            password=self.password,
            redis_port=str(self._ports["6379/tcp"]),
        )

    def django_settings(self):
        connection_info = self.connect()
        return {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": f"redis://default:{connection_info.password}@localhost:{connection_info.redis_port}",
        }

    def redis(self, **client_kwargs):
        """Get a Generic Redis Client object from the redis-py library.

        **Returns**:
        - The [Generic Redis Client](https://redis-py.readthedocs.io/en/stable/connections.html#generic-client) from the redis-py library.
        """
        _check_redis_installs()
        connection_info = self.connect()
        if self._sync_client is None:
            self._sync_client = redis.Redis(
                host="localhost",
                port=int(connection_info.redis_port),
                password=connection_info.password,
                **client_kwargs,
            )
        return self._sync_client

    async def redis_async(self, *, decode_responses: bool = True):
        """Get an Async Redis Client object from the redis-py library.

        **Returns**:
        - The [Async Redis Client object](https://redis-py.readthedocs.io/en/stable/connections.html#async-client) from the redis-py library.
        """
        _check_redis_installs()
        connection_info = await self.connect_async()
        if self._async_pool is None:
            self._async_pool = await redis.asyncio.from_url(
                f"redis://localhost:{connection_info.redis_port}",
                password=connection_info.password,
                decode_responses=decode_responses,
            )
        return self._async_pool
