from uuid import UUID

from fastapi import APIRouter

from src.dependency import (
    AuthorizedUserID,
    MemberServiceDependency,
    MixerEventServiceDependency,
    PaginationDependency,
    RemapperServiceDependency,
)
from src.domain.models.mixer.requests import CreateDraftRequest
from src.domain.models.mixer.responses import (
    DraftDetailResponse,
    DraftItemResponse,
)

from ._utils import get_access

router = APIRouter(tags=["Event Draft"])


@router.post("/{event_id}/drafts", status_code=201, response_model=DraftDetailResponse)
async def create_draft(
    user_id: AuthorizedUserID,
    server_id: UUID,
    event_id: UUID,
    body: CreateDraftRequest,
    event_service: MixerEventServiceDependency,
    member_service: MemberServiceDependency,
    remapper_service: RemapperServiceDependency,
):
    access = await get_access(server_id, user_id, member_service)
    result = await event_service.create_draft(access, event_id, body)
    return await remapper_service.map_draft_detail_response(result)


@router.get("/{event_id}/drafts", response_model=list[DraftItemResponse])
async def list_drafts(
    user_id: AuthorizedUserID,
    server_id: UUID,
    event_id: UUID,
    event_service: MixerEventServiceDependency,
    member_service: MemberServiceDependency,
    remapper_service: RemapperServiceDependency,
    pagination: PaginationDependency,
):
    access = await get_access(server_id, user_id, member_service)
    result = await event_service.list_drafts(
        access, event_id, pagination.page, pagination.page_size
    )
    return await remapper_service.map_draft_items_response(result)


@router.get("/drafts/{draft_id}", response_model=DraftDetailResponse)
async def get_draft(
    user_id: AuthorizedUserID,
    server_id: UUID,
    draft_id: UUID,
    event_service: MixerEventServiceDependency,
    member_service: MemberServiceDependency,
    remapper_service: RemapperServiceDependency,
):
    access = await get_access(server_id, user_id, member_service)
    result = await event_service.get_draft(access, draft_id)
    return await remapper_service.map_draft_detail_response(result)
