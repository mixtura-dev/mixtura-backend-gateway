from uuid import UUID

from fastapi import APIRouter

from src.dependency import (
    AuthorizedUserID,
    MemberServiceDependency,
    MixerEventServiceDependency,
    PaginationDependency,
)
from src.domain.models.mixer.request import AddOrganizerRequest
from src.domain.models.response import StatusResponse

from ._utils import get_access

router = APIRouter(tags=["Event Organizer"])


@router.get("/{event_id}/organizers", response_model=list[dict])
async def list_organizers(
    user_id: AuthorizedUserID,
    server_id: UUID,
    event_id: UUID,
    event_service: MixerEventServiceDependency,
    member_service: MemberServiceDependency,
    pagination: PaginationDependency,
):
    access = await get_access(server_id, user_id, member_service)
    return await event_service.list_organizers(
        access, event_id, pagination.page, pagination.page_size
    )


@router.post("/{event_id}/organizers", status_code=201, response_model=dict)
async def add_organizer(
    user_id: AuthorizedUserID,
    server_id: UUID,
    event_id: UUID,
    body: AddOrganizerRequest,
    event_service: MixerEventServiceDependency,
    member_service: MemberServiceDependency,
):
    access = await get_access(server_id, user_id, member_service)
    return await event_service.add_organizer(access, event_id, body.member_id)


@router.delete("/{event_id}/organizers/{member_id}", response_model=StatusResponse)
async def remove_organizer(
    user_id: AuthorizedUserID,
    server_id: UUID,
    event_id: UUID,
    member_id: UUID,
    event_service: MixerEventServiceDependency,
    member_service: MemberServiceDependency,
):
    access = await get_access(server_id, user_id, member_service)
    return await event_service.remove_organizer(access, event_id, member_id)
