# Handling imports and missing dependencies
try:
    import boto3
except ImportError:
    boto3 = None

try:
    import asyncpg
except ImportError:
    asyncpg = None

try:
    import pg8000
except ImportError:
    pg8000 = None

try:
    import psycopg2
except ImportError:
    psycopg2 = None

try:
    from sqlalchemy.ext.asyncio import create_async_engine
except ImportError:
    async_sessionmaker = None
    create_async_engine = None

try:
    from sqlalchemy import create_engine, event
except ImportError:
    event = None
    create_engine = None
    DeclarativeBase = None
    sessionmaker = None

# Importing the required modules

from launchflow.aws.resource import AWSResource
from launchflow.generic_clients import PostgresClient
from pydantic import BaseModel


# Connection information model
class RDSPostgresConnectionInfo(BaseModel):
    endpoint: str
    username: str
    password: str
    port: int
    dbname: str
    region: str


class RDSPostgres(AWSResource[RDSPostgresConnectionInfo], PostgresClient):
    """A Postgres cluster running on AWS's RDS service.

    **Example usage:**
    ```python
    from sqlalchemy import text
    import launchflow as lf

    postgres = lf.aws.RDSPostgres("my-pg-db")

    # Quick utilities for connecting to SQLAlchemy, Django, and other ORMs
    engine = postgres.sqlalchemy_engine()

    with engine.connect() as connection:
        print(connection.execute(text("SELECT 1")).fetchone())  # prints (1,)
    ```
    """

    def __init__(
        self,
        name: str,
    ) -> None:
        """Create a new RDS Postgres resource.

        **Args**:
        - `name`: The name of the RDS Postgres cluster.
        """
        super().__init__(
            name=name,
            product_name="aws_rds_postgres",
            create_args={},
        )

    def django_settings(self):
        """Returns a Django settings dictionary for connecting to the RDS Postgres instance.

        **Example usage:**
        ```python
        import launchflow as lf

        postgres = lf.aws.RDSPostgres("my-pg-db")

        # settings.py
        DATABASES = {
            # Connect Django's ORM to the RDS Postgres instance
            "default": postgres.django_settings(),
        }
        ```
        """
        if psycopg2 is None:
            raise ImportError(
                "psycopg2 is not installed. Please install it with `pip install psycopg2`."
            )

        connection_info = self.connect()
        return {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": connection_info.dbname,
            "USER": connection_info.username,
            "PASSWORD": connection_info.password,
            "HOST": connection_info.endpoint,
            "PORT": connection_info.port,
        }

    def sqlalchemy_engine_options(self):
        if pg8000 is None:
            raise ImportError(
                "pg8000 is not installed. Please install it with `pip install pg8000`."
            )

        connection_info = self.connect()
        return {
            "url": f"postgresql+pg8000://{connection_info.username}:{connection_info.password}@{connection_info.endpoint}:{connection_info.port}/{connection_info.dbname}",
        }

    async def sqlalchemy_async_engine_options(self):
        if asyncpg is None:
            raise ImportError(
                "asyncpg is not installed. Please install it with `pip install asyncpg`."
            )

        connection_info = await self.connect_async()
        return {
            "url": f"postgresql+asyncpg://{connection_info.username}:{connection_info.password}@{connection_info.endpoint}:{connection_info.port}/{connection_info.dbname}"
        }

    def sqlalchemy_engine(self, **engine_kwargs):
        """Returns a SQLAlchemy engine for connecting to the RDS SQL Postgres instance.

        Args:
        - `**engine_kwargs`: Additional keyword arguments to pass to `sqlalchemy.create_engine`.

        **Example usage:**
        ```python
        import launchflow as lf

        postgres = lf.aws.RDSPostgres("my-pg-db")

        # Creates a SQLAlchemy engine for connecting to the RDS SQL Postgres instance
        engine = postgres.sqlalchemy_engine()

        with engine.connect() as connection:
            print(connection.execute("SELECT 1").fetchone())  # prints (1,)
        ```
        """
        if create_engine is None:
            raise ImportError(
                "SQLAlchemy is not installed. Please install it with "
                "`pip install sqlalchemy`."
            )

        engine_options = self.sqlalchemy_engine_options()
        engine_options.update(engine_kwargs)

        return create_engine(**engine_options)

    async def sqlalchemy_async_engine(self, **engine_kwargs):
        """Returns an async SQLAlchemy engine for connecting to the RDS SQL Postgres instance.

        Args:
        - `**engine_kwargs`: Additional keyword arguments to pass to `create_async_engine`.

        **Example usage:**
        ```python
        import launchflow as lf

        postgres = lf.aws.RDSPostgres("my-pg-db")

        # Creates an async SQLAlchemy engine for connecting to the RDS SQL Postgres instance
        engine = await postgres.sqlalchemy_async_engine()

        async with engine.connect() as connection:
            result = await connection.execute("SELECT 1")
            print(await result.fetchone())
        ```
        """
        if create_async_engine is None:
            raise ImportError(
                "SQLAlchemy asyncio extension is not installed. "
                "Please install it with `pip install sqlalchemy[asyncio]`."
            )

        engine_options = await self.sqlalchemy_async_engine_options()
        engine_options.update(engine_kwargs)

        return create_async_engine(**engine_options)
