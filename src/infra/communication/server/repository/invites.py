from uuid import UUID
from faststream.rabbit import RabbitBroker, RabbitMessage
from ..models.request import AccessDataRequest
from src.domain.models.access import AccessData
from ..models.member.response import MemberResponse
from ..models.invites.request import (
    GetInviteByKeyRequest,
    GetInviteListRequest,
    GetUserRestrictionRequest,
    InviteCreateRequest,
    RevokeInviteRequest,
    UseInviteRequest,
)
from ..models.invites.response import InviteAdminResponse, InviteKeyResponse
from ..models.response import ErrorResponse, ResponseMessage, StatusResponse


class InviteRepository:
    def __init__(self, broker: RabbitBroker):
        self.broker = broker

    async def get_user_restriction(
        self, server_id: UUID, user_id: UUID
    ) -> ResponseMessage[int | ErrorResponse]:
        request = GetUserRestrictionRequest(user_id=user_id, server_id=server_id)
        response: RabbitMessage = await self.broker.request(
            request, queue="invite.get_restriction"
        )
        return ResponseMessage[int | ErrorResponse].model_validate_json(response.body)

    async def get_invite_info(
        self, key: str
    ) -> ResponseMessage[InviteKeyResponse | ErrorResponse]:
        request = GetInviteByKeyRequest(key=key)
        response: RabbitMessage = await self.broker.request(
            request, queue="invite.get_by_key"
        )
        return ResponseMessage[InviteKeyResponse | ErrorResponse].model_validate_json(
            response.body
        )

    async def use_invite(
        self, key: str, user_id: UUID, nickname: str, restriction_mask: int
    ) -> ResponseMessage[MemberResponse | ErrorResponse]:
        request = UseInviteRequest(
            key=key,
            user_id=user_id,
            nickname=nickname,
            restriction_mask=restriction_mask,
        )
        response: RabbitMessage = await self.broker.request(request, queue="invite.use")
        return ResponseMessage[MemberResponse | ErrorResponse].model_validate_json(
            response.body
        )

    async def list_invites(
        self, access: AccessData
    ) -> ResponseMessage[list[InviteAdminResponse] | ErrorResponse]:
        request = GetInviteListRequest(
            access_data=AccessDataRequest(
                member_id=access.member_id,
                server_id=access.server_id,
                permission_mask=access.permission_mask,
                restriction_mask=access.restriction_mask,
            )
        )
        response: RabbitMessage = await self.broker.request(
            request, queue="invite.list"
        )
        return ResponseMessage[
            list[InviteAdminResponse] | ErrorResponse
        ].model_validate_json(response.body)

    async def create_invite(
        self, access: AccessData, use_limit: int | None = None
    ) -> ResponseMessage[InviteAdminResponse | ErrorResponse]:
        request = InviteCreateRequest(
            access_data=AccessDataRequest(
                member_id=access.member_id,
                server_id=access.server_id,
                permission_mask=access.permission_mask,
                restriction_mask=access.restriction_mask,
            ),
            use_limit=use_limit,
        )
        response: RabbitMessage = await self.broker.request(
            request, queue="invite.create"
        )
        return ResponseMessage[InviteAdminResponse | ErrorResponse].model_validate_json(
            response.body
        )

    async def revoke_invite(
        self, access: AccessData, invite_id: UUID
    ) -> ResponseMessage[StatusResponse | ErrorResponse]:
        request = RevokeInviteRequest(
            access_data=AccessDataRequest(
                member_id=access.member_id,
                server_id=access.server_id,
                permission_mask=access.permission_mask,
                restriction_mask=access.restriction_mask,
            ),
            invite_id=invite_id,
        )
        response: RabbitMessage = await self.broker.request(
            request, queue="invite.revoke"
        )
        return ResponseMessage[StatusResponse | ErrorResponse].model_validate_json(
            response.body
        )
