from uuid import UUID

from fastapi import APIRouter

from src.dependency import (
    AuthorizedUserID,
    MemberServiceDependency,
    MixerEventServiceDependency,
    PaginationDependency,
)
from src.domain.models.mixer.requests import RecordMatchResultRequest, SetupMatchRequest
from src.domain.models.mixer.responses import SingleMatchViewResponse

from ._utils import get_access

router = APIRouter(tags=["Event Match"])


@router.post(
    "/{event_id}/matches", status_code=201, response_model=SingleMatchViewResponse
)
async def setup_match(
    user_id: AuthorizedUserID,
    server_id: UUID,
    event_id: UUID,
    body: SetupMatchRequest,
    event_service: MixerEventServiceDependency,
    member_service: MemberServiceDependency,
):
    access = await get_access(server_id, user_id, member_service)
    return await event_service.setup_match(access, event_id, body)


@router.get("/{event_id}/matches", response_model=list[SingleMatchViewResponse])
async def list_matches(
    user_id: AuthorizedUserID,
    server_id: UUID,
    event_id: UUID,
    event_service: MixerEventServiceDependency,
    member_service: MemberServiceDependency,
    pagination: PaginationDependency,
    active: bool | None = None,
):
    access = await get_access(server_id, user_id, member_service)
    return await event_service.list_matches(
        access, event_id, active, pagination.page, pagination.page_size
    )


@router.get("/matches/{match_id}", response_model=SingleMatchViewResponse)
async def get_match(
    user_id: AuthorizedUserID,
    server_id: UUID,
    match_id: UUID,
    event_service: MixerEventServiceDependency,
    member_service: MemberServiceDependency,
):
    access = await get_access(server_id, user_id, member_service)
    return await event_service.get_match(access, match_id)


@router.post(
    "/matches/{match_id}/result", response_model=SingleMatchViewResponse
)
async def record_match_result(
    user_id: AuthorizedUserID,
    server_id: UUID,
    match_id: UUID,
    body: RecordMatchResultRequest,
    event_service: MixerEventServiceDependency,
    member_service: MemberServiceDependency,
):
    access = await get_access(server_id, user_id, member_service)
    return await event_service.record_match_result(access, match_id, body)
