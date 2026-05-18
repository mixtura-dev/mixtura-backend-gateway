from uuid import UUID

from pydantic import BaseModel

from ..enums import EventPlayerStatus
from ..shared import AccessDataRequest, PaginationRequest


class CreateDraftRequest(BaseModel):
    access_data: AccessDataRequest
    event_id: UUID
    player_ids: list[UUID] | None = None
    statuses: list[EventPlayerStatus] | None = None
    limit: int | None = None
    pinned_only: bool = False


class GetDraftRequest(BaseModel):
    draft_id: UUID
    access_data: AccessDataRequest


class ListDraftsRequest(BaseModel):
    event_id: UUID
    access_data: AccessDataRequest
    pagination: PaginationRequest = PaginationRequest()
