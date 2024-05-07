# Handling imports and missing dependencies
try:
    import redis
except ImportError:
    redis = None

# Importing the required modules

from launchflow.aws.resource import AWSResource
from launchflow.generic_clients import RedisClient
from pydantic import BaseModel


def _check_installs():
    if redis is None:
        raise ImportError(
            "redis library is not installed. Please install it with `pip install redis`."
        )


# Connection information model
class ElasticacheRedisConnectionInfo(BaseModel):
    host: str
    port: int
    password: str


class ElasticacheRedis(AWSResource[ElasticacheRedisConnectionInfo], RedisClient):
    """A Redis cluster running on AWS's Elasticache service.

    **NOTE**: This resource can only be accessed from within the same VPC it is created in.
    Use [EC2Redis](/reference/aws-resources/ec2#ec-2-redis) to create a Redis instance that can be accessed from outside the VPC.

    **Example usage:**
    ```python
    import launchflow as lf

    elasticache = lf.aws.ElasticacheRedis("my-redis-cluster")

    # Set a key-value pair
    client = elasticache.redis()
    client.set("my-key", "my-value")

    # Async compatible
    async_client = await elasticache.redis_async()
    await async_client.set("my-key", "my-value")
    ```
    """

    def __init__(
        self,
        name: str,
    ) -> None:
        """Create a new Elasticache Redis resource.


        **Args**:
        - `name`: The name of the Elasticache Redis cluster.
        """
        super().__init__(
            name=name,
            product_name="aws_elasticache_redis",
            create_args={},
        )

    def django_settings(self):
        """Returns a Django settings dictionary for connecting to the Elasticache Redis cluster.

        **Example usage:**
        ```python
        import launchflow as lf

        elasticache = lf.aws.ElasticacheRedis("my-redis-cluster")

        # settings.py
        CACHES = {
            # Connect Django's cache backend to the Elasticache Redis cluster
            "default": elasticache.django_settings(),
        }
        ```
        """
        connection_info = self.connect()
        return {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            # NOTE: We use rediss:// to connect to a Redis cluster with TLS enabled.
            "LOCATION": f"rediss://default:{connection_info.password}@{connection_info.host}:{connection_info.port}",
        }

    def redis(self):
        """Get a Generic Redis Client object from the redis-py library.

        **Returns**:
        - The [Generic Redis Client](https://redis-py.readthedocs.io/en/stable/connections.html#generic-client) from the redis-py library.
        """
        _check_installs()
        connection_info = self.connect()
        return redis.Redis(
            host=connection_info.host,
            port=connection_info.port,
            password=connection_info.password,
            decode_responses=True,
        )

    async def redis_async(self):
        """Get an Async Redis Client object from the redis-py library.

        **Returns**:
        - The [Async Redis Client object](https://redis-py.readthedocs.io/en/stable/connections.html#async-client) from the redis-py library.
        """
        _check_installs()
        connection_info = await self.connect_async()
        return await redis.asyncio.from_url(
            # NOTE: We use rediss:// to connect to a Redis cluster with TLS enabled.
            f"rediss://{connection_info.host}:{connection_info.port}",
            password=connection_info.password,
            decode_responses=True,
        )
