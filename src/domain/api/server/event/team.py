from uuid import UUID

from fastapi import APIRouter

from src.dependency import (
    AuthorizedUserID,
    MemberServiceDependency,
    MixerEventServiceDependency,
    PaginationDependency,
)
from src.domain.models.mixer.response import TeamItemResponse

from ._utils import get_access

router = APIRouter(tags=["Event Team"])


@router.get("/{event_id}/teams", response_model=list[TeamItemResponse])
async def list_teams(
    user_id: AuthorizedUserID,
    server_id: UUID,
    event_id: UUID,
    event_service: MixerEventServiceDependency,
    member_service: MemberServiceDependency,
    pagination: PaginationDependency,
):
    access = await get_access(server_id, user_id, member_service)
    return await event_service.list_teams(
        access, event_id, pagination.page, pagination.page_size
    )
