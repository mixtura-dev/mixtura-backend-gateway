from uuid import UUID
from ..exceptions import ServiceException
from src.infra.communication.server.repository.invites import InviteRepository
from src.infra.communication.server.schemas.response import ErrorResponse
from src.infra.communication.server.schemas.invites.response import (
    InviteAdminResponse,
    InviteKeyResponse,
)
from src.infra.communication.server.schemas.member.response import MemberResponse
from src.domain.models.access import AccessData


class InviteService:
    def __init__(self, invite_repository: InviteRepository) -> None:
        self.invite_repository = invite_repository

    async def get_invite_info(self, key: str) -> InviteKeyResponse:
        response = await self.invite_repository.get_invite_info(key)
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message

    async def use_invite(
        self, key: str, user_id: UUID, nickname: str, restriction_mask: int
    ) -> MemberResponse:
        response = await self.invite_repository.use_invite(
            key, user_id, nickname, restriction_mask
        )
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message

    async def list_invites(self, access: AccessData, server_id: UUID) -> list[InviteAdminResponse]:
        response = await self.invite_repository.list_invites(access, server_id)
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message

    async def create_invite(self, access: AccessData, use_limit: int | None = None) -> InviteAdminResponse:
        response = await self.invite_repository.create_invite(access, use_limit)
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message

    async def revoke_invite(self, access: AccessData, invite_id: UUID):
        response = await self.invite_repository.revoke_invite(access, invite_id)
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message
