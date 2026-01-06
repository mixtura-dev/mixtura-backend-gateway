from uuid import UUID
from datetime import datetime

from faststream.rabbit import RabbitBroker, RabbitMessage
from ..schemas.request import AccessDataRequest
from src.domain.models.access import AccessData
from ..schemas.member.request import (
    AddMemberRestrictionRequest,
    GetMemberByUserRequest,
    GetMemberListRequest,
    GetMemberRestrictionsRequest,
    JoinServerRequest,
    KickMemberRequest,
    MemberGetInfoRequest,
    MemberMigrationRequest,
    MemberUpdateRequest,
    RemoveMemberRestrictionRequest,
    VirtualMemberCreateRequest,
)
from ..schemas.member.response import (
    AccessResponse,
    MemberResponse,
    MemberRestrictionResponse,
    RestrictionResponse,
)
from ..schemas.response import ErrorResponse, ResponseMessage, StatusResponse


class MemberRepository:
    def __init__(self, broker: RabbitBroker):
        self.broker = broker

    async def get_member_by_user(
        self, server_id: UUID, user_id: UUID
    ) -> ResponseMessage[AccessResponse | ErrorResponse]:
        request = GetMemberByUserRequest(server_id=server_id, user_id=user_id)
        response: RabbitMessage = await self.broker.request(
            request, queue="member.by_user"
        )
        return ResponseMessage[AccessResponse | ErrorResponse].model_validate_json(
            response.body
        )

    async def list_members(
        self, access: AccessData
    ) -> ResponseMessage[list[MemberResponse] | ErrorResponse]:
        request = GetMemberListRequest(access_data=AccessDataRequest(member_id=access.member_id, server_id=access.server_id, permission_mask=access.permission_mask, restriction_mask=access.restriction_mask))
        response: RabbitMessage = await self.broker.request(
            request, queue="member.list"
        )
        return ResponseMessage[
            list[MemberResponse] | ErrorResponse
        ].model_validate_json(response.body)

    async def join_server(
        self,
        server_id: UUID,
        user_id: UUID,
        nickname: str,
        restriction_mask: int,
    ) -> ResponseMessage[MemberResponse | ErrorResponse]:
        request = JoinServerRequest(
            server_id=server_id,
            user_id=user_id,
            nickname=nickname,
            restriction_mask=restriction_mask,
        )
        response: RabbitMessage = await self.broker.request(
            request, queue="member.join"
        )
        return ResponseMessage[MemberResponse | ErrorResponse].model_validate_json(
            response.body
        )

    async def create_virtual(
        self, access: AccessData, nickname: str
    ) -> ResponseMessage[MemberResponse | ErrorResponse]:
        request = VirtualMemberCreateRequest(access_data=AccessDataRequest(member_id=access.member_id, server_id=access.server_id, permission_mask=access.permission_mask, restriction_mask=access.restriction_mask), nickname=nickname)
        response: RabbitMessage = await self.broker.request(
            request, queue="member.virtual.create"
        )
        return ResponseMessage[MemberResponse | ErrorResponse].model_validate_json(
            response.body
        )

    async def get_member(
        self, access: AccessData, target_member_id: UUID
    ) -> ResponseMessage[MemberResponse | ErrorResponse]:
        request = MemberGetInfoRequest(
            access_data=AccessDataRequest(member_id=access.member_id, server_id=access.server_id, permission_mask=access.permission_mask, restriction_mask=access.restriction_mask), target_member_id=target_member_id
        )
        response: RabbitMessage = await self.broker.request(request, queue="member.get")
        return ResponseMessage[MemberResponse | ErrorResponse].model_validate_json(
            response.body
        )

    async def update_member(
        self,
        access: AccessData,
        target_member_id: UUID,
        name: str | None = None,
        server_role_id: UUID | None = None,
    ) -> ResponseMessage[MemberResponse | ErrorResponse]:
        request = MemberUpdateRequest(
            access_data=AccessDataRequest(member_id=access.member_id, server_id=access.server_id, permission_mask=access.permission_mask, restriction_mask=access.restriction_mask),
            target_member_id=target_member_id,
            name=name,
            server_role_id=server_role_id,
        )
        response: RabbitMessage = await self.broker.request(
            request, queue="member.update"
        )
        return ResponseMessage[MemberResponse | ErrorResponse].model_validate_json(
            response.body
        )

    async def kick_member(
        self, access: AccessData, target_member_id: UUID
    ) -> ResponseMessage[StatusResponse | ErrorResponse]:
        request = KickMemberRequest(
            access_data=AccessDataRequest(member_id=access.member_id, server_id=access.server_id, permission_mask=access.permission_mask, restriction_mask=access.restriction_mask), target_member_id=target_member_id
        )
        response: RabbitMessage = await self.broker.request(
            request, queue="member.kick"
        )
        return ResponseMessage[StatusResponse | ErrorResponse].model_validate_json(
            response.body
        )

    async def migrate_member(
        self,
        access: AccessData,
        origin_member_id: UUID,
        target_member_id: UUID,
    ) -> ResponseMessage[MemberResponse | ErrorResponse]:
        request = MemberMigrationRequest(
            access_data=AccessDataRequest(member_id=access.member_id, server_id=access.server_id, permission_mask=access.permission_mask, restriction_mask=access.restriction_mask),
            origin_member_id=origin_member_id,
            target_member_id=target_member_id,
        )
        response: RabbitMessage = await self.broker.request(
            request, queue="member.virtual.migrate"
        )
        return ResponseMessage[MemberResponse | ErrorResponse].model_validate_json(
            response.body
        )

    async def get_global_restrictions(
        self,
    ) -> ResponseMessage[list[RestrictionResponse] | ErrorResponse]:
        response: RabbitMessage = await self.broker.request(
            None, queue="server.global.restrictions"
        )
        return ResponseMessage[
            list[RestrictionResponse] | ErrorResponse
        ].model_validate_json(response.body)

    async def list_restrictions(
        self, access: AccessData, target_member_id: UUID
    ) -> ResponseMessage[list[MemberRestrictionResponse] | ErrorResponse]:
        request = GetMemberRestrictionsRequest(
            access_data=AccessDataRequest(member_id=access.member_id, server_id=access.server_id, permission_mask=access.permission_mask, restriction_mask=access.restriction_mask), target_member_id=target_member_id
        )
        response: RabbitMessage = await self.broker.request(
            request, queue="member.restriction.list"
        )
        return ResponseMessage[
            list[MemberRestrictionResponse] | ErrorResponse
        ].model_validate_json(response.body)

    async def add_restriction(
        self,
        access: AccessData,
        target_member_id: UUID,
        reason: str,
        expiration_date: datetime,
        restriction_id: UUID,
    ) -> ResponseMessage[MemberRestrictionResponse | ErrorResponse]:
        request = AddMemberRestrictionRequest(
            access_data=AccessDataRequest(member_id=access.member_id, server_id=access.server_id, permission_mask=access.permission_mask, restriction_mask=access.restriction_mask),
            target_member_id=target_member_id,
            reason=reason,
            expiration_date=expiration_date,
            restriction_id=restriction_id,
        )
        response: RabbitMessage = await self.broker.request(
            request, queue="member.restriction.add"
        )
        return ResponseMessage[
            MemberRestrictionResponse | ErrorResponse
        ].model_validate_json(response.body)

    async def remove_restriction(
        self,
        access: AccessData,
        target_member_id: UUID,
        member_restriction_id: UUID,
    ) -> ResponseMessage[StatusResponse | ErrorResponse]:
        request = RemoveMemberRestrictionRequest(
            access_data=AccessDataRequest(member_id=access.member_id, server_id=access.server_id, permission_mask=access.permission_mask, restriction_mask=access.restriction_mask),
            target_member_id=target_member_id,
            member_restriction_id=member_restriction_id,
        )
        response: RabbitMessage = await self.broker.request(
            request, queue="member.restriction.remove"
        )
        return ResponseMessage[StatusResponse | ErrorResponse].model_validate_json(
            response.body
        )
