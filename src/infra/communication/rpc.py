import logging
from typing import Any

from src.domain.exceptions import RabbitTimeoutException
from src.infra.communication.rabbit import RabbitRpcClient, RpcResponse

logger = logging.getLogger(__name__)


async def rpc_request(
    client: RabbitRpcClient,
    request: Any,
    *,
    queue: str,
    timeout: float | None = None,
) -> RpcResponse:
    return await client.request(
        queue=queue,
        payload=request,
        timeout=timeout,
    )
