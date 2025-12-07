from uuid import UUID
from fastapi import Cookie, Request, Depends, Response

from .domain.exceptions import ServiceException

from .domain.service.auth import AuthService

from .infra.communication.auth.repository import AuthRepository

from .infra.redis import RedisSessionManager, RedisRepository
from typing import Annotated
from redis.asyncio import Redis
from faststream.rabbit.fastapi import RabbitBroker
import logging

logger = logging.getLogger(__name__)


async def get_redis_session(request: Request):
    if not hasattr(request.app.state, "redis_manager"):
        logger.error("redis_manager not found in app.state")
        raise RuntimeError("Redis session manager not configured")
    redis_manager: RedisSessionManager = request.app.state.redis_manager
    async with redis_manager.client() as redis:
        yield redis


async def get_broker(request: Request):
    return request.app.state.rabbit_router.broker


async def get_redis_repository(redis: Annotated[Redis, Depends(get_redis_session)]):
    return RedisRepository(redis)


async def get_auth_repository(broker=Depends(get_broker)):
    return AuthRepository(broker)


AuthRepositoryDependency = Annotated[AuthRepository, Depends(get_auth_repository)]


async def get_auth_service(auth_repository: AuthRepositoryDependency):
    return AuthService(auth_repository)


AuthServiceDependency = Annotated[AuthService, Depends(get_auth_service)]


async def require_auth(
    response: Response,
    auth_service: AuthServiceDependency,
    token: str | None = Cookie(None),
):
    if token is None:
        raise ServiceException(401, "Unauthorized")
    user_Id = await auth_service.get_user_from_auth_optional(token)
    if user_Id is None:
        response.delete_cookie("token")
        raise ServiceException(401, "Unauthorized")
    return user_Id


AuthorizedUserID = Annotated[UUID, Depends(require_auth)]
