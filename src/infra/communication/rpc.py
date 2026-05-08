import logging

from faststream.rabbit import RabbitBroker

from src.env_config import env
from src.domain.exceptions import RabbitTimeoutException

logger = logging.getLogger(__name__)


async def rpc_request(
    broker: RabbitBroker,
    request,
    queue: str,
    timeout: int | None = None,
):
    if timeout is None:
        timeout = env.rabbit.request_timeout
    try:
        return await broker.request(request, queue=queue, timeout=timeout)
    except TimeoutError:
        logger.warning("RPC call to queue '%s' timed out after %ds", queue, timeout)
        raise RabbitTimeoutException()
