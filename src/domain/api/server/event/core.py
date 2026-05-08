from uuid import UUID

from fastapi import APIRouter

from src.dependency import (
    AuthorizedUserID,
    MemberServiceDependency,
    MixerEventServiceDependency,
    PaginationDependency,
)
from src.domain.models.mixer.request import CreateEventRequest, UpdateEventRequest
from src.domain.models.mixer.response import EventCardResponse, EventDetailResponse

from ._utils import get_access

router = APIRouter(tags=["Event Core"])


@router.get("/", response_model=list[EventCardResponse])
async def list_public_events(
    server_id: UUID,
    event_service: MixerEventServiceDependency,
    pagination: PaginationDependency,
):
    return await event_service.list_public_events(
        server_id, pagination.page, pagination.page_size
    )


@router.get("/private", response_model=list[EventDetailResponse])
async def list_private_events(
    user_id: AuthorizedUserID,
    server_id: UUID,
    event_service: MixerEventServiceDependency,
    member_service: MemberServiceDependency,
    pagination: PaginationDependency,
):
    access = await get_access(server_id, user_id, member_service)
    return await event_service.list_private_events(
        access, pagination.page, pagination.page_size
    )


@router.post("/", status_code=201, response_model=EventCardResponse)
async def create_event(
    user_id: AuthorizedUserID,
    server_id: UUID,
    body: CreateEventRequest,
    event_service: MixerEventServiceDependency,
    member_service: MemberServiceDependency,
):
    access = await get_access(server_id, user_id, member_service)
    return await event_service.create_event(access, body)


@router.get("/{event_id}", response_model=EventCardResponse | EventDetailResponse)
async def get_event(
    user_id: AuthorizedUserID,
    server_id: UUID,
    event_id: UUID,
    event_service: MixerEventServiceDependency,
    member_service: MemberServiceDependency,
):
    access = await get_access(server_id, user_id, member_service)
    return await event_service.get_event(access, event_id)


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
