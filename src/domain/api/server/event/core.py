from uuid import UUID

from fastapi import APIRouter

from src.dependency import (
    AuthorizedUserID,
    MemberServiceDependency,
    MixerEventServiceDependency,
    PaginationDependency,
    RemapperServiceDependency,
)
from src.domain.models.mixer.request import (
    CreateEventRequest,
    UpdateEventRequest,
    AddIntegrationRequest,
    AddGameRoleRequest,
    UpdateGameRoleRequest,
)
from src.domain.models.mixer.response import EventCardResponse, EventDetailResponse
from src.domain.models.server.member.response import ReducedMemberResponse

from ._utils import get_access

router = APIRouter(tags=["Event Core"])


async def _enrich_event_organizers(event, access, member_service, remapper_service):
    if not event.organizers:
        return event
    member_ids = {org.member_id for org in event.organizers}
    member_info: dict[UUID, ReducedMemberResponse] = {}
    for member_id in member_ids:
        try:
            info = await member_service.get_member(access, member_id)
            if info:
                member_info[member_id] = ReducedMemberResponse.model_validate(info)
        except Exception:
            pass
    event.organizers = await remapper_service.map_event_detail_organizers(
        event.organizers, member_info
    )
    return event


@router.get("/", response_model=list[EventCardResponse])
async def list_events(
    server_id: UUID,
    event_service: MixerEventServiceDependency,
    user_id: AuthorizedUserID,
    member_service: MemberServiceDependency,
):
    access = await get_access(server_id, user_id, member_service)
    return await event_service.list_events(server_id, access)


@router.post("/", status_code=201, response_model=EventDetailResponse)
async def create_event(
    user_id: AuthorizedUserID,
    server_id: UUID,
    body: CreateEventRequest,
    event_service: MixerEventServiceDependency,
    member_service: MemberServiceDependency,
    remapper_service: RemapperServiceDependency,
):
    access = await get_access(server_id, user_id, member_service)
    result = await event_service.create_event(access, body)
    return await _enrich_event_organizers(result, access, member_service, remapper_service)


@router.get("/{event_id}", response_model=EventDetailResponse)
async def get_event(
    user_id: AuthorizedUserID,
    server_id: UUID,
    event_id: UUID,
    event_service: MixerEventServiceDependency,
    member_service: MemberServiceDependency,
    remapper_service: RemapperServiceDependency,
):
    access = await get_access(server_id, user_id, member_service)
    result = await event_service.get_event(access, event_id)
    return await _enrich_event_organizers(result, access, member_service, remapper_service)


@router.patch("/{event_id}", response_model=EventDetailResponse)
async def update_event(
    user_id: AuthorizedUserID,
    server_id: UUID,
    event_id: UUID,
    body: UpdateEventRequest,
    event_service: MixerEventServiceDependency,
    member_service: MemberServiceDependency,
):
    access = await get_access(server_id, user_id, member_service)
    return await event_service.update_event(access, event_id, body)


@router.post("/{event_id}/activate", response_model=EventDetailResponse)
async def activate_event(
    user_id: AuthorizedUserID,
    server_id: UUID,
    event_id: UUID,
    event_service: MixerEventServiceDependency,
    member_service: MemberServiceDependency,
):
    access = await get_access(server_id, user_id, member_service)
    return await event_service.activate_event(access, event_id)


@router.post("/{event_id}/registration/open", response_model=EventDetailResponse)
async def open_registration(
    user_id: AuthorizedUserID,
    server_id: UUID,
    event_id: UUID,
    event_service: MixerEventServiceDependency,
    member_service: MemberServiceDependency,
):
    access = await get_access(server_id, user_id, member_service)
    return await event_service.open_registration(access, event_id)


@router.post("/{event_id}/registration/close", response_model=EventDetailResponse)
async def close_registration(
    user_id: AuthorizedUserID,
    server_id: UUID,
    event_id: UUID,
    event_service: MixerEventServiceDependency,
    member_service: MemberServiceDependency,
):
    access = await get_access(server_id, user_id, member_service)
    return await event_service.close_registration(access, event_id)


@router.post("/{event_id}/cancel", response_model=EventDetailResponse)
async def cancel_event(
    user_id: AuthorizedUserID,
    server_id: UUID,
    event_id: UUID,
    event_service: MixerEventServiceDependency,
    member_service: MemberServiceDependency,
):
    access = await get_access(server_id, user_id, member_service)
    return await event_service.cancel_event(access, event_id)


@router.post("/{event_id}/complete", response_model=EventDetailResponse)
async def complete_event(
    user_id: AuthorizedUserID,
    server_id: UUID,
    event_id: UUID,
    event_service: MixerEventServiceDependency,
    member_service: MemberServiceDependency,
):
    access = await get_access(server_id, user_id, member_service)
    return await event_service.complete_event(access, event_id)


@router.post("/{event_id}/integrations", response_model=EventDetailResponse)
async def add_integration(
    user_id: AuthorizedUserID,
    server_id: UUID,
    event_id: UUID,
    body: AddIntegrationRequest,
    event_service: MixerEventServiceDependency,
    member_service: MemberServiceDependency,
):
    access = await get_access(server_id, user_id, member_service)
    return await event_service.add_integration(access, event_id, body.name)


@router.delete("/{event_id}/integrations/{integration_id}", response_model=EventDetailResponse)
async def remove_integration(
    user_id: AuthorizedUserID,
    server_id: UUID,
    event_id: UUID,
    integration_id: UUID,
    event_service: MixerEventServiceDependency,
    member_service: MemberServiceDependency,
):
    access = await get_access(server_id, user_id, member_service)
    return await event_service.remove_integration(access, event_id, integration_id)


@router.post("/{event_id}/roles", response_model=EventDetailResponse)
async def add_game_role(
    user_id: AuthorizedUserID,
    server_id: UUID,
    event_id: UUID,
    body: AddGameRoleRequest,
    event_service: MixerEventServiceDependency,
    member_service: MemberServiceDependency,
):
    access = await get_access(server_id, user_id, member_service)
    return await event_service.add_game_role(
        access, event_id, body.game_role_id, body.override_max_count, body.override_min_count
    )


@router.patch("/{event_id}/roles/{selected_role_id}", response_model=EventDetailResponse)
async def update_game_role(
    user_id: AuthorizedUserID,
    server_id: UUID,
    event_id: UUID,
    selected_role_id: UUID,
    body: UpdateGameRoleRequest,
    event_service: MixerEventServiceDependency,
    member_service: MemberServiceDependency,
):
    access = await get_access(server_id, user_id, member_service)
    return await event_service.update_game_role(
        access, event_id, selected_role_id, body.override_max_count, body.override_min_count
    )


@router.delete("/{event_id}/roles/{selected_role_id}", response_model=EventDetailResponse)
async def remove_game_role(
    user_id: AuthorizedUserID,
    server_id: UUID,
    event_id: UUID,
    selected_role_id: UUID,
    event_service: MixerEventServiceDependency,
    member_service: MemberServiceDependency,
):
    access = await get_access(server_id, user_id, member_service)
    return await event_service.remove_game_role(access, event_id, selected_role_id)
