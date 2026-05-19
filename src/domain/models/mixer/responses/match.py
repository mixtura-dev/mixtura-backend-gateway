from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class SingleMatchSlotViewResponse(BaseModel):
    slot_id: UUID
    slot_num: int
    team_id: UUID
    score_id: UUID
    score: int


class SingleMatchViewResponse(BaseModel):
    event_id: UUID
    bracket_id: UUID
    stage_id: UUID
    group_id: UUID
    match_id: UUID
    match_index: int
    draft_id: UUID | None = None
    completed_at: datetime | None = None
    slots: list[SingleMatchSlotViewResponse]
