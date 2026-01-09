from uuid import UUID
from datetime import datetime

from ...infra.communication.server.models.request import PaginationRequest
from ..exceptions import ServiceException
from src.infra.communication.server.repository.member import MemberRepository
from src.infra.communication.server.models.response import ErrorResponse
from src.domain.models.access import AccessData


class MemberService:
    def __init__(self, member_repository: MemberRepository) -> None:
        self.member_repository = member_repository

    async def get_member_by_user(self, server_id: UUID, user_id: UUID) -> AccessData:
        response = await self.member_repository.get_member_by_user(server_id, user_id)
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        access = AccessData(
            user_id=user_id,
            member_id=response.message.member.id if response.message.member else None,
            server_id=server_id,
            permission_mask=response.message.permission_mask,
            restriction_mask=response.message.restriction_mask,
        )
        return access

    async def list_members(
        self, access: AccessData, nickname_filter: str, page: int, page_size: int
    ):
        if access.member_id is None:
            raise ServiceException(400, "The user must be a member of the server")
        response = await self.member_repository.list_members(
            access, PaginationRequest(page=page, page_size=page_size), nickname_filter
        )
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message

    async def join_server(
        self, server_id: UUID, user_id: UUID, nickname: str, restriction_mask: int
    ):
        response = await self.member_repository.join_server(
            server_id, user_id, nickname, restriction_mask
        )
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message

    async def create_virtual(self, access: AccessData, nickname: str):
        if access.member_id is None:
            raise ServiceException(400, "The user must be a member of the server")
        response = await self.member_repository.create_virtual(access, nickname)
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message

    async def get_member(self, access: AccessData, target_member_id: UUID):
        if access.member_id is None:
            raise ServiceException(400, "The user must be a member of the server")
        response = await self.member_repository.get_member(access, target_member_id)
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message

    async def get_member_permissions(self, access: AccessData):
        if access.member_id is None:
            raise ServiceException(400, "The user must be a member of the server")
        response = await self.member_repository.get_member_permissions(access)
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message

    async def update_member(
        self,
        access: AccessData,
        target_member_id: UUID,
        name: str | None,
        server_role_id: UUID | None,
    ):
        if access.member_id is None:
            raise ServiceException(400, "The user must be a member of the server")
        response = await self.member_repository.update_member(
            access, target_member_id, name, server_role_id
        )
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message

    async def kick_member(self, access: AccessData, target_member_id: UUID):
        if access.member_id is None:
            raise ServiceException(400, "The user must be a member of the server")
        response = await self.member_repository.kick_member(access, target_member_id)
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message

    async def migrate_member(
        self, access: AccessData, origin_member_id: UUID, target_member_id: UUID
    ):
        if access.member_id is None:
            raise ServiceException(400, "The user must be a member of the server")
        response = await self.member_repository.migrate_member(
            access, origin_member_id, target_member_id
        )
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message

    async def get_global_restrictions(self):
        response = await self.member_repository.get_global_restrictions()
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message

    async def list_restrictions(self, access: AccessData, target_member_id: UUID):
        if access.member_id is None:
            raise ServiceException(400, "The user must be a member of the server")
        response = await self.member_repository.list_restrictions(
            access, target_member_id
        )
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message

    async def add_restriction(
        self,
        access: AccessData,
        target_member_id: UUID,
        reason: str,
        expiration_date: datetime,
        restriction_id: UUID,
    ):
        if access.member_id is None:
            raise ServiceException(400, "The user must be a member of the server")
        response = await self.member_repository.add_restriction(
            access, target_member_id, reason, expiration_date, restriction_id
        )
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message

    async def remove_restriction(
        self, access: AccessData, target_member_id: UUID, member_restriction_id: UUID
    ):
        if access.member_id is None:
            raise ServiceException(400, "The user must be a member of the server")
        response = await self.member_repository.remove_restriction(
            access, target_member_id, member_restriction_id
        )
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message
