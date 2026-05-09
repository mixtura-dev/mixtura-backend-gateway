from uuid import UUID

from fastapi import APIRouter

from src.dependency import (
    AuthorizedUserID,
    MemberServiceDependency,
    MixerEventServiceDependency,
    PaginationDependency,
)
from src.domain.models.mixer.request import (
    ApplicationStatus,
    ReviewApplicationRequest,
    SubmitApplicationRequest,
    AddCustomFieldRequest,
    UpdateCustomFieldRequest,
    UpdateTimeSettingsRequest,
)
from src.domain.models.mixer.response import EventDetailResponse

from ._utils import get_access

router = APIRouter(tags=["Event Application"])


@router.post("/{event_id}/applications", status_code=201, response_model=dict)
async def submit_application(
    user_id: AuthorizedUserID,
    server_id: UUID,
    event_id: UUID,
    body: SubmitApplicationRequest,
    event_service: MixerEventServiceDependency,
    member_service: MemberServiceDependency,
):
    access = await get_access(server_id, user_id, member_service)
    return await event_service.submit_application(access, event_id, body)


@router.get("/{event_id}/applications", response_model=list[dict])
async def list_applications(
    user_id: AuthorizedUserID,
    server_id: UUID,
    event_id: UUID,
    event_service: MixerEventServiceDependency,
    member_service: MemberServiceDependency,
    pagination: PaginationDependency,
    status: ApplicationStatus | None = None,
):
    access = await get_access(server_id, user_id, member_service)
    return await event_service.list_applications(
        access, event_id, status, pagination.page, pagination.page_size
    )


@router.get("/applications/{application_id}", response_model=dict)
async def get_application(
    user_id: AuthorizedUserID,
    server_id: UUID,
    application_id: UUID,
    event_service: MixerEventServiceDependency,
    member_service: MemberServiceDependency,
):
    access = await get_access(server_id, user_id, member_service)
    return await event_service.get_application(access, application_id)


@router.patch("/applications/{application_id}/review", response_model=dict)
async def review_application(
    user_id: AuthorizedUserID,
    server_id: UUID,
    application_id: UUID,
    body: ReviewApplicationRequest,
    event_service: MixerEventServiceDependency,
    member_service: MemberServiceDependency,
):
    access = await get_access(server_id, user_id, member_service)
    return await event_service.review_application(access, application_id, body)


@router.get("/{event_id}/applications/form", response_model=dict)
async def get_application_form_settings(
    server_id: UUID,
    event_id: UUID,
    event_service: MixerEventServiceDependency,
    member_service: MemberServiceDependency,
    user_id: AuthorizedUserID | None = None,
):
    access = None
    if user_id:
        access = await get_access(server_id, user_id, member_service)
    return await event_service.get_application_form_settings(event_id, access)


@router.post("/{event_id}/applications/fields", response_model=EventDetailResponse)
async def add_custom_field(
    user_id: AuthorizedUserID,
    server_id: UUID,
    event_id: UUID,
    body: AddCustomFieldRequest,
    event_service: MixerEventServiceDependency,
    member_service: MemberServiceDependency,
):
    access = await get_access(server_id, user_id, member_service)
    return await event_service.add_custom_field(
        access, event_id, body.name, body.is_private, body.is_required
    )


@router.patch("/{event_id}/applications/fields/{field_id}", response_model=EventDetailResponse)
async def update_custom_field(
    user_id: AuthorizedUserID,
    server_id: UUID,
    event_id: UUID,
    field_id: UUID,
    body: UpdateCustomFieldRequest,
    event_service: MixerEventServiceDependency,
    member_service: MemberServiceDependency,
):
    access = await get_access(server_id, user_id, member_service)
    return await event_service.update_custom_field(
        access, event_id, field_id, body.name, body.is_private, body.is_required
    )


@router.delete("/{event_id}/applications/fields/{field_id}", response_model=EventDetailResponse)
async def remove_custom_field(
    user_id: AuthorizedUserID,
    server_id: UUID,
    event_id: UUID,
    field_id: UUID,
    event_service: MixerEventServiceDependency,
    member_service: MemberServiceDependency,
):
    access = await get_access(server_id, user_id, member_service)
    return await event_service.remove_custom_field(access, event_id, field_id)


@router.patch("/{event_id}/applications/time_settings", response_model=EventDetailResponse)
async def update_time_settings(
    user_id: AuthorizedUserID,
    server_id: UUID,
    event_id: UUID,
    body: UpdateTimeSettingsRequest,
    event_service: MixerEventServiceDependency,
    member_service: MemberServiceDependency,
):
    access = await get_access(server_id, user_id, member_service)
    return await event_service.update_time_settings(access, event_id, body)
