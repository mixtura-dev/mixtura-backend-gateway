from uuid import UUID

from pydantic import BaseModel, Field


class TeamItemResponse(BaseModel):
    id: UUID
    event_id: UUID
    draft_id: UUID | None = None
    name: str


class TeamPlayerItemResponse(BaseModel):
    id: UUID
    team_id: UUID
    member_id: UUID
    game_role_id: UUID
    rating: float


class TeamDetailResponse(BaseModel):
    id: UUID
    event_id: UUID
    draft_id: UUID | None = None
    name: str
    players: list[TeamPlayerItemResponse] = Field(default_factory=list)
