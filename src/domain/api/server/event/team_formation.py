from uuid import UUID

from fastapi import APIRouter

from src.dependency import (
    AuthorizedUserID,
    MemberServiceDependency,
    MixerEventServiceDependency,
    PaginationDependency,
)
from src.domain.models.mixer.requests import RunTeamFormationRequest
from src.domain.models.mixer.responses import (
    TeamDetailResponse,
    TeamFormationJobResponse,
)

from ._utils import get_access

router = APIRouter(tags=["Event Team Formation"])


@router.post(
    "/drafts/{draft_id}/team-formation", response_model=TeamFormationJobResponse
)
async def run_team_formation(
    user_id: AuthorizedUserID,
    server_id: UUID,
    draft_id: UUID,
    body: RunTeamFormationRequest,
    event_service: MixerEventServiceDependency,
    member_service: MemberServiceDependency,
):
    access = await get_access(server_id, user_id, member_service)
    return await event_service.run_team_formation(access, draft_id, body)


@router.get(
    "/drafts/{draft_id}/team-formation", response_model=TeamFormationJobResponse
)
async def get_team_formation(
    user_id: AuthorizedUserID,
    server_id: UUID,
    draft_id: UUID,
    event_service: MixerEventServiceDependency,
    member_service: MemberServiceDependency,
    pagination: PaginationDependency,
):
    access = await get_access(server_id, user_id, member_service)
    return await event_service.get_team_formation(
        access, draft_id, pagination.page, pagination.page_size
    )


@router.post(
    "/drafts/{draft_id}/team-formation/variants/{variant_id}/choose",
    response_model=list[TeamDetailResponse],
)
async def choose_team_formation_variant(
    user_id: AuthorizedUserID,
    server_id: UUID,
    draft_id: UUID,
    variant_id: UUID,
    event_service: MixerEventServiceDependency,
    member_service: MemberServiceDependency,
):
    access = await get_access(server_id, user_id, member_service)
    return await event_service.choose_team_formation_variant(access, draft_id, variant_id)
