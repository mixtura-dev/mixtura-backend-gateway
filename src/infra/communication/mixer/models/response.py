from datetime import datetime
from enum import Enum
from typing import Generic, TypeVar
from uuid import UUID

from pydantic import BaseModel, Field

T = TypeVar("T")


class ResponseMessage(BaseModel, Generic[T]):
    status: int
    message: T


class ErrorResponse(BaseModel):
    message: str


class StatusResponse(BaseModel):
    status: str = Field(default="ok")


class EventMatchType(str, Enum):
    SINGLE = "SINGLE"
    TOURNAMENT = "TOURNAMENT"


class EventStatus(str, Enum):
    CREATED = "CREATED"
    REGISTRATION = "REGISTRATION"
    IDLE = "IDLE"
    FORMATION = "FORMATION"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class TeamFormation(str, Enum):
    DRAFT = "DRAFT"
    BALANCE = "BALANCE"
    MANUAL = "MANUAL"


class ApplicationStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    WAITLIST = "WAITLIST"


class EventCard(BaseModel):
    id: UUID
    name: str
    match_type: EventMatchType
    use_application: bool
    is_public: bool
    team_size: int
    team_formation: TeamFormation
    status: EventStatus
    server_id: UUID


class OrganizerData(BaseModel):
    id: UUID
    member_id: UUID


class OrganizerItem(BaseModel):
    id: UUID
    event_id: UUID
    member_id: UUID


class RequiredIntegrationData(BaseModel):
    id: UUID
    name: str


class SelectedGameRoleData(BaseModel):
    id: UUID
    game_role_id: UUID
    override_max_count: int | None = None
    override_min_count: int | None = None


class ApplicationTimeSettingsData(BaseModel):
    id: UUID
    start_time: datetime | None = None
    end_time: datetime | None = None


class ApplicationCustomFieldData(BaseModel):
    id: UUID
    name: str
    is_private: bool
    is_required: bool


class EventDetail(BaseModel):
    id: UUID
    name: str
    match_type: EventMatchType
    use_application: bool
    is_public: bool
    team_size: int
    team_formation: TeamFormation
    status: EventStatus
    allow_multiple_drafts: bool
    rating_set_id: UUID | None
    server_id: UUID
    organizers: list[OrganizerData] = []
    required_integrations: list[RequiredIntegrationData] = []
    selected_game_roles: list[SelectedGameRoleData] = []
    time_settings: ApplicationTimeSettingsData | None = None
    custom_fields: list[ApplicationCustomFieldData] = []


class ApplicationRoleItem(BaseModel):
    role_id: UUID
    game_role_id: UUID | None = None
    priority: int


class ApplicationIntegrationItem(BaseModel):
    integration_id: UUID
    provider_id: UUID
    provider_name: str


class ApplicationFilledFieldItem(BaseModel):
    custom_field_id: UUID
    value: str


class ApplicationRolePriorityItem(BaseModel):
    role_id: UUID
    priority: int


class ApplicationSubmitResult(BaseModel):
    id: UUID
    status: ApplicationStatus
    auto_approved: bool
    player_id: UUID


class ApplicationReviewResult(BaseModel):
    id: UUID
    status: ApplicationStatus
    player_id: UUID | None = None


class ApplicationDetail(BaseModel):
    id: UUID
    event_id: UUID
    member_id: UUID
    status: ApplicationStatus
    role_priorities: list[ApplicationRolePriorityItem] = Field(default_factory=list)
    filled_fields: list[ApplicationFilledFieldItem] = Field(default_factory=list)
    integrations: list[ApplicationIntegrationItem] = Field(default_factory=list)
    event_player_id: UUID | None = None


class ApplicationListItem(BaseModel):
    id: UUID
    member_id: UUID
    status: ApplicationStatus
    is_approved: bool
    created_at: datetime
    roles: list[ApplicationRoleItem] = Field(default_factory=list)
    integrations: list[ApplicationIntegrationItem] = Field(default_factory=list)


class ApplicationFormSettings(BaseModel):
    event_id: UUID
    event_name: str
    required_integrations: list[RequiredIntegrationData] = Field(default_factory=list)
    available_roles: list[SelectedGameRoleData] = Field(default_factory=list)
    custom_fields: list[ApplicationCustomFieldData] = Field(default_factory=list)
    time_settings: ApplicationTimeSettingsData | None = None


class RatingSnapshotPlayer(BaseModel):
    member_id: UUID
    event_player_id: UUID
    game_role_id: UUID
    priority: int
    open_rating: float
    calculated_rating: float
    effective_rating: float | None = None
    rating_source: str = "open"


class TeamFormationVariantTeam(BaseModel):
    team_index: int
    name: str
    member_ids: list[UUID]
    event_player_ids: list[UUID]
    game_role_ids: list[UUID]
    calculated_ratings: list[float]


class TeamFormationVariantMetrics(BaseModel):
    strength_diff: float = 0.0
    role_fit: float = 0.0
    rating_spread: float = 0.0
    constraint_violations: int = 0
    raw_metrics: dict[str, float] = Field(default_factory=dict)


class TeamFormationVariant(BaseModel):
    id: UUID
    draft_id: UUID
    teams: list[TeamFormationVariantTeam] = Field(default_factory=list)
    metrics: TeamFormationVariantMetrics = Field(default_factory=TeamFormationVariantMetrics)
    is_selected: bool = False


class TeamFormationJob(BaseModel):
    job_id: UUID
    draft_id: UUID
    event_id: UUID
    status: str
    variants: list[TeamFormationVariant] = Field(default_factory=list)
    rating_snapshot: list[RatingSnapshotPlayer] = Field(default_factory=list)
    error: str | None = None


class SingleMatchSlotView(BaseModel):
    slot_id: UUID
    slot_num: int
    team_id: UUID
    score_id: UUID
    score: int


class SingleMatchView(BaseModel):
    event_id: UUID
    bracket_id: UUID
    stage_id: UUID
    group_id: UUID
    match_id: UUID
    match_index: int
    draft_id: UUID | None = None
    completed_at: datetime | None = None
    result_snapshot: dict | None = None
    slots: list[SingleMatchSlotView]


class RecordedMatchResult(BaseModel):
    match: SingleMatchView
    winner_team_id: UUID | None = None
    loser_team_ids: list[UUID] = Field(default_factory=list)
    is_draw: bool = False
    forfeit_team_ids: list[UUID] = Field(default_factory=list)
    team_ranks: list[float]
    rating_payload: dict
    rating_published: bool
