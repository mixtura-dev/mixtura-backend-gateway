from uuid import UUID
from fastapi import Cookie, Request, Depends, Response

from .domain.service.remapper import RemapperService

from .domain.exceptions import ServiceException

from .domain.service.auth import AuthService

from .infra.communication.auth.repository import AuthRepository
from .infra.communication.server.repository import (
    ServerCoreRepository,
    ServerGameRepository,
    InviteRepository,
    MemberRepository,
    GameRoleRepository,
    RatingRepository,
    ServerRoleRepository,
    MemberCustomRepository,
)


from .domain.service.core import ServerCoreService
from .domain.service.games import ServerGamesService
from .domain.service.invites import InviteService
from .domain.service.member import MemberService
from .domain.service.game_roles import GameRoleService
from .domain.service.rating import RatingService
from .domain.service.roles import ServerRoleService
from .domain.service.custom import MemberCustomService

from .infra.redis import RedisSessionManager, RedisRepository
from typing import Annotated
from redis.asyncio import Redis
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


# --- Server repositories ---
async def get_server_core_repository(broker=Depends(get_broker)):
    return ServerCoreRepository(broker)


ServerCoreRepositoryDependency = Annotated[
    ServerCoreRepository, Depends(get_server_core_repository)
]


async def get_server_games_repository(broker=Depends(get_broker)):
    return ServerGameRepository(broker)


ServerGamesRepositoryDependency = Annotated[
    ServerGameRepository, Depends(get_server_games_repository)
]


async def get_invite_repository(broker=Depends(get_broker)):
    return InviteRepository(broker)


InviteRepositoryDependency = Annotated[InviteRepository, Depends(get_invite_repository)]


async def get_member_repository(broker=Depends(get_broker)):
    return MemberRepository(broker)


MemberRepositoryDependency = Annotated[MemberRepository, Depends(get_member_repository)]


async def get_game_role_repository(broker=Depends(get_broker)):
    return GameRoleRepository(broker)


GameRoleRepositoryDependency = Annotated[
    GameRoleRepository, Depends(get_game_role_repository)
]


async def get_rating_repository(broker=Depends(get_broker)):
    return RatingRepository(broker)


RatingRepositoryDependency = Annotated[RatingRepository, Depends(get_rating_repository)]


async def get_server_role_repository(broker=Depends(get_broker)):
    return ServerRoleRepository(broker)


ServerRoleRepositoryDependency = Annotated[
    ServerRoleRepository, Depends(get_server_role_repository)
]


async def get_custom_repository(broker=Depends(get_broker)):
    return MemberCustomRepository(broker)


MemberCustomRepositoryDependency = Annotated[
    MemberCustomRepository, Depends(get_custom_repository)
]


async def get_server_core_service(core_repo: ServerCoreRepositoryDependency):
    return ServerCoreService(core_repo)


ServerCoreServiceDependency = Annotated[
    ServerCoreService, Depends(get_server_core_service)
]


async def get_server_games_service(games_repo: ServerGamesRepositoryDependency):
    return ServerGamesService(games_repo)


ServerGamesServiceDependency = Annotated[
    ServerGamesService, Depends(get_server_games_service)
]


async def get_invite_service(invite_repo: InviteRepositoryDependency):
    return InviteService(invite_repo)


InviteServiceDependency = Annotated[InviteService, Depends(get_invite_service)]


async def get_member_service(member_repo: MemberRepositoryDependency):
    return MemberService(member_repo)


MemberServiceDependency = Annotated[MemberService, Depends(get_member_service)]


async def get_game_role_service(role_repo: GameRoleRepositoryDependency):
    return GameRoleService(role_repo)


GameRoleServiceDependency = Annotated[GameRoleService, Depends(get_game_role_service)]


async def get_rating_service(rating_repo: RatingRepositoryDependency):
    return RatingService(rating_repo)


RatingServiceDependency = Annotated[RatingService, Depends(get_rating_service)]


async def get_server_role_service(role_repo: ServerRoleRepositoryDependency):
    return ServerRoleService(role_repo)


ServerRoleServiceDependency = Annotated[
    ServerRoleService, Depends(get_server_role_service)
]


async def get_member_custom_service(custom_repo: MemberCustomRepositoryDependency):
    return MemberCustomService(custom_repo)


MemberCustomServiceDependency = Annotated[
    MemberCustomService, Depends(get_member_custom_service)
]

async def get_remapper_service():
    return RemapperService()

RemapperServiceDependency = Annotated[RemapperService, Depends(get_remapper_service)]

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

