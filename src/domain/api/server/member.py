from uuid import UUID
from fastapi_controllers import Controller, get, patch, post, delete

from ....dependency import (
    AuthServiceDependency,
    AuthorizedUserID,
    InviteServiceDependency,
    MemberServiceDependency,
    PaginationDependency,
)
from src.domain.models.server.member.request import (
    MemberRestrictionCreateRequest,
    MemberUpdateRequest,
    MigrationRequest,
    VirtualMemberCreateRequest,
)
from src.domain.models.server.member.response import (
    MemberResponse,
    MemberRestrictionResponse,
    ReducedMemberResponse,
)
from src.domain.models.response import StatusResponse


class MemberController(Controller):
    prefix = "/{server_id}/members"
    tags = ["Member"]

    def __init__(self, user_id: AuthorizedUserID) -> None:
        self.user_id = user_id

    @get("/", response_model=list[ReducedMemberResponse])
    async def list_members(
        self,
        server_id: UUID,
        member_service: MemberServiceDependency,
        pagination: PaginationDependency,
        query: str = "",
    ):
        access = await member_service.get_member_by_user(server_id, self.user_id)
        members = await member_service.list_members(
            access, query, pagination.page, pagination.page_size
        )
        return members

    @post("/", response_model=MemberResponse)
    async def join_server(
        self,
        server_id: UUID,
        member_service: MemberServiceDependency,
        invite_service: InviteServiceDependency,
        auth_service: AuthServiceDependency,
    ):
        user_info = await auth_service.get_user(self.user_id)
        restriction_mask = await invite_service.get_user_restriction(
            server_id, self.user_id
        )
        member = await member_service.join_server(
            server_id, self.user_id, user_info.username, restriction_mask
        )
        return member

    @post("/virtual", response_model=MemberResponse)
    async def create_virtual(
        self,
        server_id: UUID,
        body: VirtualMemberCreateRequest,
        member_service: MemberServiceDependency,
    ):
        access = await member_service.get_member_by_user(server_id, self.user_id)
        member = await member_service.create_virtual(access, body.nickname)
        return member

    @get("/{member_id}", response_model=MemberResponse)
    async def get_member(
        self,
        server_id: UUID,
        member_id: UUID,
        member_service: MemberServiceDependency,
    ):
        access = await member_service.get_member_by_user(server_id, self.user_id)
        member = await member_service.get_member(access, member_id)
        return member

    @patch("/{member_id}", response_model=MemberResponse)
    async def update_member(
        self,
        server_id: UUID,
        member_id: UUID,
        body: MemberUpdateRequest,
        member_service: MemberServiceDependency,
    ):
        access = await member_service.get_member_by_user(server_id, self.user_id)
        member = await member_service.update_member(
            access, member_id, body.name, body.server_role_id
        )
        return member

    @delete("/{member_id}", response_model=StatusResponse)
    async def kick_member(
        self,
        server_id: UUID,
        member_id: UUID,
        member_service: MemberServiceDependency,
    ):
        access = await member_service.get_member_by_user(server_id, self.user_id)
        await member_service.kick_member(access, member_id)
        return StatusResponse()

    @post("/{member_id}/migrate", response_model=MemberResponse)
    async def migrate_member(
        self,
        server_id: UUID,
        member_id: UUID,
        body: MigrationRequest,
        member_service: MemberServiceDependency,
    ):
        access = await member_service.get_member_by_user(server_id, self.user_id)
        member = await member_service.migrate_member(
            access, member_id, body.target_member_id
        )
        return member

    @get("/{member_id}/restrictions", response_model=list[MemberRestrictionResponse])
    async def get_restrictions(
        self,
        server_id: UUID,
        member_id: UUID,
        member_service: MemberServiceDependency,
    ):
        access = await member_service.get_member_by_user(server_id, self.user_id)
        restrictions = await member_service.list_restrictions(access, member_id)
        return restrictions

    @post("/{member_id}/restrictions", response_model=MemberRestrictionResponse)
    async def add_restriction(
        self,
        server_id: UUID,
        member_id: UUID,
        body: MemberRestrictionCreateRequest,
        member_service: MemberServiceDependency,
    ):
        access = await member_service.get_member_by_user(server_id, self.user_id)
        restriction = await member_service.add_restriction(
            access,
            member_id,
            body.reason,
            body.expiration_date,
            body.restriction_id,
        )
        return restriction

    @delete(
        "/{member_id}/restrictions/{member_restriction_id}",
        response_model=StatusResponse,
    )
    async def remove_restriction(
        self,
        server_id: UUID,
        member_id: UUID,
        member_restriction_id: UUID,
        member_service: MemberServiceDependency,
    ):
        access = await member_service.get_member_by_user(server_id, self.user_id)
        await member_service.remove_restriction(
            access, member_id, member_restriction_id
        )
        return StatusResponse()
