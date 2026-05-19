from uuid import UUID

from pydantic import BaseModel, Field

from ..enums import DraftStatus


class DraftedPlayerItemResponse(BaseModel):
    id: UUID
    draft_id: UUID
    event_player_id: UUID
    is_captain: bool | None = None


class DraftDetailResponse(BaseModel):
    id: UUID
    event_id: UUID
    status: DraftStatus
    drafted_players: list[DraftedPlayerItemResponse] = Field(default_factory=list)


class DraftItemResponse(BaseModel):
    id: UUID
    event_id: UUID
    status: DraftStatus
