from uuid import UUID
from faststream.rabbit import RabbitBroker, RabbitMessage
from ..schemas.request import AccessDataRequest
from ..schemas.member.response import MemberResponse
from ..schemas.invites.request import (
    GetInviteByKeyRequest,
    GetInviteListRequest,
    InviteCreateRequest,
    RevokeInviteRequest,
    UseInviteRequest,
)
from ..schemas.invites.response import InviteAdminResponse, InviteKeyResponse
from ..schemas.response import ErrorResponse, ResponseMessage, StatusResponse


class InviteRepository:
    def __init__(self, broker: RabbitBroker):
        self.broker = broker

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
        self, access_data: AccessDataRequest, server_id: UUID
    ) -> ResponseMessage[list[InviteAdminResponse] | ErrorResponse]:
        request = GetInviteListRequest(access_data=access_data, server_id=server_id)
        response: RabbitMessage = await self.broker.request(
            request, queue="invite.list"
        )
        return ResponseMessage[
            list[InviteAdminResponse] | ErrorResponse
        ].model_validate_json(response.body)

    async def create_invite(
        self, access_data: AccessDataRequest, use_limit: int | None = None
    ) -> ResponseMessage[InviteAdminResponse | ErrorResponse]:
        request = InviteCreateRequest(access_data=access_data, use_limit=use_limit)
        response: RabbitMessage = await self.broker.request(
            request, queue="invite.create"
        )
        return ResponseMessage[InviteAdminResponse | ErrorResponse].model_validate_json(
            response.body
        )

    async def revoke_invite(
        self, access_data: AccessDataRequest, invite_id: UUID
    ) -> ResponseMessage[StatusResponse | ErrorResponse]:
        request = RevokeInviteRequest(access_data=access_data, invite_id=invite_id)
        response: RabbitMessage = await self.broker.request(
            request, queue="invite.revoke"
        )
        return ResponseMessage[StatusResponse | ErrorResponse].model_validate_json(
            response.body
        )
