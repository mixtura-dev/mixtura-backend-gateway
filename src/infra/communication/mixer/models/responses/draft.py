from uuid import UUID

from pydantic import BaseModel, Field

from ..enums import DraftStatus


class DraftedPlayerItem(BaseModel):
    id: UUID
    draft_id: UUID
    event_player_id: UUID
    is_captain: bool | None = None


class DraftDetail(BaseModel):
    id: UUID
    event_id: UUID
    status: DraftStatus
    drafted_players: list[DraftedPlayerItem] = Field(default_factory=list)


class DraftItem(BaseModel):
    id: UUID
    event_id: UUID
    status: DraftStatus
