from uuid import UUID
from ..exceptions import ServiceException
from src.infra.communication.server.repository.custom import MemberCustomRepository
from src.infra.communication.server.models.response import ErrorResponse
from src.domain.models.access import AccessData


class MemberCustomService:
    def __init__(self, custom_repository: MemberCustomRepository) -> None:
        self.custom_repository = custom_repository

    async def get_customs_by_member(self, access: AccessData, target_member_id: UUID):
        response = await self.custom_repository.get_customs_by_member(access, target_member_id)
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message

    async def create_custom(self, access: AccessData, target_member_id: UUID):
        response = await self.custom_repository.create_custom(access, target_member_id)
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message

    async def delete_custom(self, access: AccessData, custom_id: UUID):
        response = await self.custom_repository.delete_custom(access, custom_id)
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message

    async def update_custom(self, access: AccessData, custom_id: UUID, game_role_id: UUID, rating: int):
        response = await self.custom_repository.update_custom(access, custom_id, game_role_id, rating)
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message
