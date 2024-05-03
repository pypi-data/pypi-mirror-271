import contextlib
from typing import Optional

from .client import LaunchFlowAsyncClient


@contextlib.asynccontextmanager
async def async_launchflow_client_ctx(api_key: Optional[str] = None):
    launchflow_async_client = LaunchFlowAsyncClient(api_key=api_key)
    try:
        yield launchflow_async_client
    finally:
        await launchflow_async_client.close()
