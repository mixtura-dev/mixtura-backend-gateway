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
)

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
