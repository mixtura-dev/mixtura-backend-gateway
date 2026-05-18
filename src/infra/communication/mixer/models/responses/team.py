from uuid import UUID

from pydantic import BaseModel, Field


class TeamItem(BaseModel):
    id: UUID
    event_id: UUID
    draft_id: UUID | None = None
    name: str


class TeamPlayerItem(BaseModel):
    id: UUID
    team_id: UUID
    member_id: UUID
    game_role_id: UUID
    rating: float


class TeamDetail(BaseModel):
    id: UUID
    event_id: UUID
    draft_id: UUID | None = None
    name: str
    players: list[TeamPlayerItem] = Field(default_factory=list)
