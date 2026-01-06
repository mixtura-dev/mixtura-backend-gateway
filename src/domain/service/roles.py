from uuid import UUID
from ..exceptions import ServiceException
from src.infra.communication.server.repository.roles import ServerRoleRepository
from src.infra.communication.server.schemas.response import ErrorResponse
from src.domain.models.access import AccessData


class ServerRoleService:
    def __init__(self, role_repository: ServerRoleRepository) -> None:
        self.role_repository = role_repository

    async def get_global_permissions(self):
        response = await self.role_repository.get_global_permissions()
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message

    async def list_roles(self, access: AccessData):
        response = await self.role_repository.list_roles(access)
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message

    async def create_role(self, access: AccessData, name: str, position: int, permission_mask: int):
        response = await self.role_repository.create_role(access, name, position, permission_mask)
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message

    async def update_role(self, access: AccessData, role_id: UUID, target_permissions_ids: list[UUID], **kwargs):
        response = await self.role_repository.update_role(access, role_id, target_permissions_ids, **kwargs)
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message

    async def update_role_permission(self, access: AccessData, role_id: UUID, target_permissions_ids: list[UUID]):
        response = await self.role_repository.update_role_permission(access, role_id, target_permissions_ids)
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message

    async def delete_role(self, access: AccessData, role_id: UUID):
        response = await self.role_repository.delete_role(access, role_id)
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message
