from uuid import UUID
from ..exceptions import ServiceException
from src.infra.communication.server.repository.game_roles import GameRoleRepository
from src.infra.communication.server.models.response import ErrorResponse
from src.domain.models.access import AccessData


class GameRoleService:
    def __init__(self, role_repository: GameRoleRepository) -> None:
        self.role_repository = role_repository

    async def get_global_role_templates(self):
        response = await self.role_repository.get_global_role_templates()
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message

    async def get_role_set(self, access: AccessData):
        response = await self.role_repository.get_role_set(access)
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message

    async def update_role_set(
        self, access: AccessData, role_set_id: UUID, name: str | None = None
    ):
        response = await self.role_repository.update_role_set(access, role_set_id, name)
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message

    async def create_role(
        self,
        access: AccessData,
        role_set_id: UUID,
        name: str,
        min_in_team: int,
        max_in_team: int,
        hidden: bool = False,
        icon_id: UUID | None = None,
    ):
        response = await self.role_repository.create_role(
            access, role_set_id, name, min_in_team, max_in_team, hidden, icon_id
        )
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message

    async def update_role(self, access: AccessData, role_id: UUID, **kwargs):
        response = await self.role_repository.update_role(access, role_id, **kwargs)
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message

    async def delete_role_icon(self, access: AccessData, role_id: UUID):
        response = await self.role_repository.delete_role_icon(access, role_id)
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message

    async def delete_role(self, access: AccessData, role_id: UUID):
        response = await self.role_repository.delete_role(access, role_id)
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message
