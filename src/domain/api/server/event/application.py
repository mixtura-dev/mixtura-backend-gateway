from typing import TypedDict
from uuid import UUID

from fastapi import APIRouter

from src.dependency import (
    AuthorizedUserID,
    AuthServiceDependency,
    MemberServiceDependency,
    MixerEventServiceDependency,
    PaginationDependency,
    RemapperServiceDependency,
)
from src.domain.models.mixer.request import (
    ApplicationStatus,
    ReviewApplicationRequest,
    SubmitApplicationRequest,
    AddCustomFieldRequest,
    UpdateCustomFieldRequest,
    UpdateTimeSettingsRequest,
)
from src.domain.models.mixer.response import (
    ApplicationDetailResponse,
    ApplicationFormSettingsResponse,
    ApplicationListItemResponse,
    EventDetailResponse,
    ReviewApplicationResponse,
    SubmitApplicationResponse,
)
from src.domain.models.server.member.response import ReducedMemberResponse

from ._utils import get_access


class _RawApplication(TypedDict):
    id: str
    member_id: str
    status: str
    is_approved: bool
    created_at: str


router = APIRouter(tags=["Event Application"])


@router.post("/{event_id}/applications", status_code=201, response_model=SubmitApplicationResponse)
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


@router.get("/{event_id}/applications", response_model=list[ApplicationListItemResponse])
async def list_applications(
    user_id: AuthorizedUserID,
    server_id: UUID,
    event_id: UUID,
    event_service: MixerEventServiceDependency,
    member_service: MemberServiceDependency,
    auth_service: AuthServiceDependency,
    remapper_service: RemapperServiceDependency,
    pagination: PaginationDependency,
    status: ApplicationStatus | None = None,
    sort_by: str = "created_at",
    sort_order: str = "desc",
):
    access = await get_access(server_id, user_id, member_service)
    applications = await event_service.list_applications(
        access, event_id, status, pagination.page, pagination.page_size, sort_by, sort_order
    )

    unique_member_ids = {UUID(app["member_id"]) for app in applications if app.get("member_id")}
    member_info: dict[UUID, ReducedMemberResponse] = {}
    for member_id in unique_member_ids:
        try:
            info = await member_service.get_member(access, member_id)
            if info:
                member_info[member_id] = ReducedMemberResponse.model_validate(info)
        except Exception:
            pass

    user_ids = {m.user_id for m in member_info.values() if m.user_id}
    user_info: dict[UUID, object] = {}
    if user_ids:
        try:
            bulk_result = await auth_service.get_users_bulk(list(user_ids))
            if isinstance(bulk_result, dict):
                user_info = dict(bulk_result)
        except Exception:
            pass

    return await remapper_service.map_applications_response(applications, member_info, user_info)


@router.get("/applications/{application_id}", response_model=ApplicationDetailResponse)
async def get_application(
    user_id: AuthorizedUserID,
    server_id: UUID,
    application_id: UUID,
    event_service: MixerEventServiceDependency,
    member_service: MemberServiceDependency,
):
    access = await get_access(server_id, user_id, member_service)
    return await event_service.get_application(access, application_id)


@router.patch("/applications/{application_id}/review", response_model=ReviewApplicationResponse)
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


@router.get("/{event_id}/applications/form", response_model=ApplicationFormSettingsResponse)
async def get_application_form_settings(
    user_id: AuthorizedUserID,
    server_id: UUID,
    event_id: UUID,
    event_service: MixerEventServiceDependency,
    member_service: MemberServiceDependency,
):
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
