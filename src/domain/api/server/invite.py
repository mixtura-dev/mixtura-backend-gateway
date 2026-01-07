from uuid import UUID
from fastapi_controllers import Controller, get, post, delete

from ....dependency import (
    AuthServiceDependency,
    AuthorizedUserID,
    InviteServiceDependency,
    MemberServiceDependency,
)
from src.domain.models.server.invites.request import InviteCreateRequest
from src.domain.models.server.invites.response import (
    InviteAdminResponse,
    InviteKeyResponse,
)
from src.domain.models.server.member.response import MemberResponse
from src.domain.models.response import StatusResponse


class ServerInviteController(Controller):
    prefix = ""
    tags = ["Server invite"]

    def __init__(self, user_id: AuthorizedUserID) -> None:
        self.user_id = user_id

    @get("/invites/{key}", response_model=InviteKeyResponse)
    async def get_invite_info(self, key: str, invite_service: InviteServiceDependency):
        invite_info = await invite_service.get_invite_info(key)
        return invite_info

    @post("/invites/{key}", response_model=MemberResponse)
    async def use_invite(
        self,
        key: str,
        invite_service: InviteServiceDependency,
        auth_service: AuthServiceDependency,
    ):
        invite_info = await invite_service.get_invite_info(key)
        user_info = await auth_service.get_user(self.user_id)
        restriction_mask = await invite_service.get_user_restriction(
            invite_info.server.id, self.user_id
        )
        member = await invite_service.use_invite(
            key, self.user_id, user_info.username, restriction_mask
        )
        return member

    @get("/{server_id}/invites", response_model=list[InviteAdminResponse])
    async def list_invites(
        self,
        server_id: UUID,
        member_service: MemberServiceDependency,
        invite_service: InviteServiceDependency,
    ):
        access = await member_service.get_member_by_user(server_id, self.user_id)
        invites = await invite_service.list_invites(access)
        return invites

    @post("/{server_id}/invites", response_model=InviteAdminResponse)
    async def create_invite(
        self,
        server_id: UUID,
        body: InviteCreateRequest,
        member_service: MemberServiceDependency,
        invite_service: InviteServiceDependency,
    ):
        access = await member_service.get_member_by_user(server_id, self.user_id)
        invite = await invite_service.create_invite(access, body.use_limit)
        return invite

    @delete("/{server_id}/invites/{invite_id}", response_model=StatusResponse)
    async def revoke_invite(
        self,
        server_id: UUID,
        invite_id: UUID,
        member_service: MemberServiceDependency,
        invite_service: InviteServiceDependency,
    ):
        access = await member_service.get_member_by_user(server_id, self.user_id)
        await invite_service.revoke_invite(access, invite_id)
        return StatusResponse()
