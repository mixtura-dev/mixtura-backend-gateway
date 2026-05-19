from uuid import UUID

from pydantic import BaseModel, Field


class RatingSnapshotPlayerResponse(BaseModel):
    member_id: UUID
    event_player_id: UUID
    game_role_id: UUID
    priority: int
    open_rating: float
    calculated_rating: float
    effective_rating: float | None = None
    rating_source: str = "open"


class TeamFormationVariantTeamResponse(BaseModel):
    team_index: int
    name: str
    member_ids: list[UUID]
    event_player_ids: list[UUID]
    game_role_ids: list[UUID]
    calculated_ratings: list[float]


class TeamFormationVariantMetricsResponse(BaseModel):
    strength_diff: float = 0.0
    role_fit: float = 0.0
    rating_spread: float = 0.0
    constraint_violations: int = 0
    raw_metrics: dict[str, float] = Field(default_factory=dict)


class TeamFormationVariantResponse(BaseModel):
    id: UUID
    draft_id: UUID
    teams: list[TeamFormationVariantTeamResponse] = Field(default_factory=list)
    metrics: TeamFormationVariantMetricsResponse = Field(
        default_factory=TeamFormationVariantMetricsResponse
    )
    is_selected: bool = False


class TeamFormationJobResponse(BaseModel):
    job_id: UUID
    draft_id: UUID
    event_id: UUID
    status: str
    variants: list[TeamFormationVariantResponse] = Field(default_factory=list)
    rating_snapshot: list[RatingSnapshotPlayerResponse] = Field(default_factory=list)
    error: str | None = None
