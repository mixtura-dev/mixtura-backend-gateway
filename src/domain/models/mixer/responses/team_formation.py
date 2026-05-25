from uuid import UUID

from pydantic import BaseModel, Field


class RatingSnapshotPlayerResponse(BaseModel):
    member_id: UUID
    event_player_id: UUID
    game_role_id: UUID
    priority: int
    open_rating: float
    rating_source: str = "open"


class TeamFormationVariantTeamResponse(BaseModel):
    team_index: int
    name: str
    member_ids: list[UUID]
    event_player_ids: list[UUID]
    game_role_ids: list[UUID]
    calculated_ratings: list[float]


class MixQualityMetricsResponse(BaseModel):
    uniformity: float
    fairness: float
    role_points: float
    role_fairness: float


class TournamentQualityMetricsResponse(BaseModel):
    dp_fairness: float = 0.0
    dp_role_fairness: float = 0.0
    vq_uniformity: float = 0.0
    role_priority_points: float = 0.0
    fitness_balance: float = 0.0
    fitness_priority: float = 0.0
    fitness_role_imbalance: float = 0.0
    fitness_team_spread: float = 0.0
    fitness_subrole: float = 0.0
    role_subrole_penalty: float = 0.0
    evaluation: float = 0.0


class TeamFormationVariantResponse(BaseModel):
    id: UUID
    draft_id: UUID
    teams: list[TeamFormationVariantTeamResponse] = Field(default_factory=list)
    metrics: MixQualityMetricsResponse | TournamentQualityMetricsResponse = Field(
        default_factory=TournamentQualityMetricsResponse
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
