from uuid import UUID
from ..exceptions import ServiceException
from src.infra.communication.server.repository.core import ServerCoreRepository
from src.infra.communication.server.models.response import ErrorResponse
from src.infra.communication.server.models.core.response import (
    ServerDetailResponse,
    ServerListResponse,
)
from src.domain.models.access import AccessData


class ServerCoreService:
    def __init__(self, core_repository: ServerCoreRepository) -> None:
        self.core_repository = core_repository

    async def get_public_servers(self) -> list[ServerListResponse]:
        response = await self.core_repository.get_public_servers()
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message

    async def get_user_servers(self, user_id: UUID) -> list[ServerListResponse]:
        response = await self.core_repository.get_user_servers(user_id)
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message

    async def create_server(
        self,
        user_id: UUID,
        user_name: str,
        name: str,
        public: bool,
        description: str = "",
        rating_set_id: UUID | None = None,
        role_set_id: UUID | None = None,
    ) -> ServerDetailResponse:
        response = await self.core_repository.create_server(
            user_id, user_name, name, public, description, rating_set_id, role_set_id
        )
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message

    async def get_server(self, access: AccessData) -> ServerDetailResponse:
        response = await self.core_repository.get_server(access)
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message

    async def update_server(self, access: AccessData, **kwargs) -> ServerDetailResponse:
        response = await self.core_repository.update_server(access, **kwargs)
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message

    async def delete_banner(self, access: AccessData):
        response = await self.core_repository.delete_banner(access)
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message

    async def delete_icon(self, access: AccessData):
        response = await self.core_repository.delete_icon(access)
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message

    async def delete_server(self, access: AccessData):
        response = await self.core_repository.delete_server(access)
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message
