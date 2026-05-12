from uuid import UUID

from fastapi import APIRouter

from src.dependency import (
    AuthorizedUserID,
    MemberServiceDependency,
    MixerEventServiceDependency,
    PaginationDependency,
)
from src.domain.models.mixer.request import AddOrganizerRequest
from src.domain.models.mixer.response import (
    OrganizerItemResponse,
    OrganizerListItemResponse,
)
from src.domain.models.response import StatusResponse
from src.domain.models.server.member.response import ReducedMemberResponse

from ._utils import get_access

router = APIRouter(tags=["Event Organizer"])


@router.get("/{event_id}/organizers", response_model=list[OrganizerListItemResponse])
async def list_organizers(
    user_id: AuthorizedUserID,
    server_id: UUID,
    event_id: UUID,
    event_service: MixerEventServiceDependency,
    member_service: MemberServiceDependency,
    pagination: PaginationDependency,
):
    access = await get_access(server_id, user_id, member_service)
    organizers = await event_service.list_organizers(
        access, event_id, pagination.page, pagination.page_size
    )

    members: dict[UUID, ReducedMemberResponse] = {}
    for organizer in organizers:
        if organizer.member_id in members:
            continue
        member = await member_service.get_member(access, organizer.member_id)
        members[organizer.member_id] = ReducedMemberResponse.model_validate(member)

    return [
        OrganizerListItemResponse(member=members[organizer.member_id])
        for organizer in organizers
    ]


@router.post("/{event_id}/organizers", status_code=201, response_model=OrganizerItemResponse)
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
