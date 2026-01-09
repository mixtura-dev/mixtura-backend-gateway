from uuid import UUID
from fastapi import APIRouter
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

member_router = APIRouter(
    prefix="/{server_id}/members",
    tags=["Member"],
)


@member_router.get("/", response_model=list[ReducedMemberResponse])
async def list_members(
    user_id: AuthorizedUserID,
    server_id: UUID,
    member_service: MemberServiceDependency,
    pagination: PaginationDependency,
    query: str = "",
):
    access = await member_service.get_member_by_user(server_id, user_id)
    members = await member_service.list_members(
        access, query, pagination.page, pagination.page_size
    )
    return members


@member_router.post("/", response_model=MemberResponse)
async def join_server(
    user_id: AuthorizedUserID,
    server_id: UUID,
    member_service: MemberServiceDependency,
    invite_service: InviteServiceDependency,
    auth_service: AuthServiceDependency,
):
    user_info = await auth_service.get_user(user_id)
    restriction_mask = await invite_service.get_user_restriction(server_id, user_id)
    member = await member_service.join_server(
        server_id, user_id, user_info.username, restriction_mask
    )
    return member


@member_router.post("/virtual", response_model=MemberResponse)
async def create_virtual(
    user_id: AuthorizedUserID,
    server_id: UUID,
    body: VirtualMemberCreateRequest,
    member_service: MemberServiceDependency,
):
    access = await member_service.get_member_by_user(server_id, user_id)
    member = await member_service.create_virtual(access, body.nickname)
    return member


@member_router.get("/me", response_model=MemberResponse)
async def get_my_member(
    user_id: AuthorizedUserID,
    server_id: UUID,
    member_service: MemberServiceDependency,
):
    access = await member_service.get_member_by_user(server_id, user_id)
    if access.member_id is None:
        raise Exception("The user is not a member of the server")
    member = await member_service.get_member(access, access.member_id)
    return member


@member_router.get("/{member_id}", response_model=MemberResponse)
async def get_member(
    user_id: AuthorizedUserID,
    server_id: UUID,
    member_id: UUID,
    member_service: MemberServiceDependency,
):
    access = await member_service.get_member_by_user(server_id, user_id)
    member = await member_service.get_member(access, member_id)
    return member


@member_router.patch("/{member_id}", response_model=MemberResponse)
async def update_member(
    user_id: AuthorizedUserID,
    server_id: UUID,
    member_id: UUID,
    body: MemberUpdateRequest,
    member_service: MemberServiceDependency,
):
    access = await member_service.get_member_by_user(server_id, user_id)
    member = await member_service.update_member(
        access, member_id, body.name, body.server_role_id
    )
    return member


@member_router.delete("/{member_id}", response_model=StatusResponse)
async def kick_member(
    user_id: AuthorizedUserID,
    server_id: UUID,
    member_id: UUID,
    member_service: MemberServiceDependency,
):
    access = await member_service.get_member_by_user(server_id, user_id)
    await member_service.kick_member(access, member_id)
    return StatusResponse()


@member_router.post("/{member_id}/migrate", response_model=MemberResponse)
async def migrate_member(
    user_id: AuthorizedUserID,
    server_id: UUID,
    member_id: UUID,
    body: MigrationRequest,
    member_service: MemberServiceDependency,
):
    access = await member_service.get_member_by_user(server_id, user_id)
    member = await member_service.migrate_member(
        access, member_id, body.target_member_id
    )
    return member


@member_router.get(
    "/{member_id}/restrictions", response_model=list[MemberRestrictionResponse]
)
async def get_restrictions(
    user_id: AuthorizedUserID,
    server_id: UUID,
    member_id: UUID,
    member_service: MemberServiceDependency,
):
    access = await member_service.get_member_by_user(server_id, user_id)
    restrictions = await member_service.list_restrictions(access, member_id)
    return restrictions


@member_router.post(
    "/{member_id}/restrictions", response_model=MemberRestrictionResponse
)
async def add_restriction(
    user_id: AuthorizedUserID,
    server_id: UUID,
    member_id: UUID,
    body: MemberRestrictionCreateRequest,
    member_service: MemberServiceDependency,
):
    access = await member_service.get_member_by_user(server_id, user_id)
    restriction = await member_service.add_restriction(
        access,
        member_id,
        body.reason,
        body.expiration_date,
        body.restriction_id,
    )
    return restriction


@member_router.delete(
    "/{member_id}/restrictions/{member_restriction_id}",
    response_model=StatusResponse,
)
async def remove_restriction(
    user_id: AuthorizedUserID,
    server_id: UUID,
    member_id: UUID,
    member_restriction_id: UUID,
    member_service: MemberServiceDependency,
):
    access = await member_service.get_member_by_user(server_id, user_id)
    await member_service.remove_restriction(access, member_id, member_restriction_id)
    return StatusResponse()
