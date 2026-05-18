from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from ..shared import AccessDataRequest, PaginationRequest


class SetupMatchRequest(BaseModel):
    access_data: AccessDataRequest
    event_id: UUID
    team_ids: list[UUID]
    draft_id: UUID | None = None
    scheduled_at: datetime | None = None


class RecordMatchResultRequest(BaseModel):
    access_data: AccessDataRequest
    match_id: UUID
    scores: dict[UUID, int]


class GetMatchRequest(BaseModel):
    match_id: UUID
    access_data: AccessDataRequest


class ListMatchesRequest(BaseModel):
    event_id: UUID
    access_data: AccessDataRequest
    active: bool | None = None
    pagination: PaginationRequest = PaginationRequest()
