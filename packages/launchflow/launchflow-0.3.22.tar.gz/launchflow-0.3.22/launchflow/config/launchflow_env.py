import os
from dataclasses import dataclass
from typing import Optional


def get_boolean_variable(name: str, default_value: Optional[bool] = None) -> bool:
    true_ = ("true", '1')
    false_ = ("false", '0')
    value: str | None = os.getenv(name, None)
    if value is None:
        if default_value is None:
            raise ValueError(f"Required variable `{name}` not set!")
        else:
            value = str(default_value)
    if value.lower() not in true_ + false_:
        raise ValueError(f"Invalid value `{value}` for variable `{name}`")
    return value.lower() in true_


@dataclass
class LaunchFlowEnvVars:
    project: Optional[str]
    cloud_provider: Optional[str]
    environment: Optional[str]
    api_key: Optional[str] = None
    connection_bucket: Optional[str] = None
    connection_path: Optional[str] = None
    local_mode_enabled: Optional[bool] = False

    @classmethod
    def load_from_env(cls):
        """
        Loads the object's properties from environment variables.

        Returns:
            An instance of LaunchFlowDotEnv with properties populated from environment variables.
        """
        project = os.getenv("LAUNCHFLOW_PROJECT", None)
        cloud_provider = os.getenv("LAUNCHFLOW_CLOUD_PROVIDER", None)
        environment = os.getenv("LAUNCHFLOW_ENVIRONMENT", None)
        api_key = os.getenv("LAUNCHFLOW_API_KEY", None)
        connection_bucket = os.getenv("LAUNCHFLOW_CONNECTION_BUCKET", None)
        connection_path = os.getenv("LAUNCHFLOW_CONNECTION_PATH", None)
        local_mode_enabled = get_boolean_variable("LAUNCHFLOW_LOCAL_MODE_ENABLED", False)

        return cls(
            project=project,
            cloud_provider=cloud_provider,
            environment=environment,
            api_key=api_key,
            connection_bucket=connection_bucket,
            connection_path=connection_path,
            local_mode_enabled=local_mode_enabled,
        )


launchflow_env_vars = None


# NOTE: We use a global variable so its only loaded once
def load_launchflow_env():
    global launchflow_env_vars
    if launchflow_env_vars is None:
        launchflow_env_vars = LaunchFlowEnvVars.load_from_env()
    return launchflow_env_vars
