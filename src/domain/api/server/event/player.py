from uuid import UUID

from fastapi import APIRouter

from src.dependency import (
    AuthorizedUserID,
    MemberServiceDependency,
    MixerEventServiceDependency,
    PaginationDependency,
)
from src.domain.models.mixer.request import EventPlayerStatus, UpdatePlayerStatusRequest
from src.domain.models.response import StatusResponse

from ._utils import get_access

router = APIRouter(tags=["Event Player"])


@router.get("/{event_id}/players", response_model=list[dict])
async def list_players(
    user_id: AuthorizedUserID,
    server_id: UUID,
    event_id: UUID,
    event_service: MixerEventServiceDependency,
    member_service: MemberServiceDependency,
    pagination: PaginationDependency,
    status: EventPlayerStatus | None = None,
):
    access = await get_access(server_id, user_id, member_service)
    return await event_service.list_players(
        access, event_id, status, pagination.page, pagination.page_size
    )


@router.patch("/{event_id}/players/{member_id}/status", response_model=dict)
async def update_player_status(
    user_id: AuthorizedUserID,
    server_id: UUID,
    event_id: UUID,
    member_id: UUID,
    body: UpdatePlayerStatusRequest,
    event_service: MixerEventServiceDependency,
    member_service: MemberServiceDependency,
):
    access = await get_access(server_id, user_id, member_service)
    return await event_service.update_player_status(access, event_id, member_id, body)


@router.delete("/{event_id}/players/{member_id}", response_model=StatusResponse)
async def remove_player(
    user_id: AuthorizedUserID,
    server_id: UUID,
    event_id: UUID,
    member_id: UUID,
    event_service: MixerEventServiceDependency,
    member_service: MemberServiceDependency,
):
    access = await get_access(server_id, user_id, member_service)
    return await event_service.remove_player(access, event_id, member_id)
