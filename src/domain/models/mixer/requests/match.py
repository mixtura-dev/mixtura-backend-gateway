from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class SetupMatchRequest(BaseModel):
    team_ids: list[UUID]
    draft_id: UUID | None = None
    scheduled_at: datetime | None = None


class RecordMatchResultRequest(BaseModel):
    scores: dict[UUID, int]
