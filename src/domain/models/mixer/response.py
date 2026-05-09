from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


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


class OrganizerResponse(BaseModel):
    id: UUID
    member_id: UUID


class RequiredIntegrationResponse(BaseModel):
    id: UUID
    name: str


class SelectedGameRoleResponse(BaseModel):
    id: UUID
    game_role_id: UUID
    override_max_count: int | None = None
    override_min_count: int | None = None


class ApplicationTimeSettingsResponse(BaseModel):
    id: UUID
    start_time: datetime | None = None
    end_time: datetime | None = None


class ApplicationCustomFieldResponse(BaseModel):
    id: UUID
    name: str
    is_private: bool
    is_required: bool


class EventCardResponse(BaseModel):
    id: UUID
    name: str
    match_type: EventMatchType
    use_application: bool
    is_public: bool
    team_size: int
    team_formation: TeamFormation
    status: EventStatus
    server_id: UUID


class EventDetailResponse(BaseModel):
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
    organizers: list[OrganizerResponse] = []
    required_integrations: list[RequiredIntegrationResponse] = []
    selected_game_roles: list[SelectedGameRoleResponse] = []
    time_settings: ApplicationTimeSettingsResponse | None = None
    custom_fields: list[ApplicationCustomFieldResponse] = []


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
    result_snapshot: dict | None = None
    slots: list[SingleMatchSlotViewResponse]


class RecordedMatchResultResponse(BaseModel):
    match: SingleMatchViewResponse
    winner_team_id: UUID | None = None
    loser_team_ids: list[UUID] = Field(default_factory=list)
    is_draw: bool = False
    forfeit_team_ids: list[UUID] = Field(default_factory=list)
    team_ranks: list[float]
    rating_payload: dict
    rating_published: bool


class ApplicationStatusResponse(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    WAITLIST = "WAITLIST"


class SubmitApplicationResponse(BaseModel):
    id: UUID
    status: ApplicationStatusResponse
    auto_approved: bool
    player_id: UUID | None = None


class ApplicationListItemUserResponse(BaseModel):
    id: UUID
    username: str | None = None


class ApplicationListItemResponse(BaseModel):
    id: UUID
    member_id: UUID
    status: ApplicationStatusResponse
    is_approved: bool
    created_at: datetime
    user: ApplicationListItemUserResponse | None = None


class ApplicationFilledFieldResponse(BaseModel):
    custom_field_id: UUID
    value: str


class ApplicationIntegrationResponse(BaseModel):
    user_provider_id: UUID


class ApplicationDetailResponse(BaseModel):
    id: UUID
    event_id: UUID
    member_id: UUID
    status: ApplicationStatusResponse
    role_priorities: dict[str, int] = Field(default_factory=dict)
    filled_fields: list[ApplicationFilledFieldResponse] = Field(default_factory=list)
    integrations: list[ApplicationIntegrationResponse] = Field(default_factory=list)
    event_player_id: UUID | None = None


class ReviewApplicationResponse(BaseModel):
    id: UUID
    status: ApplicationStatusResponse
    player_id: UUID | None = None


class ApplicationFormIntegrationResponse(BaseModel):
    id: UUID
    name: str


class ApplicationFormRoleResponse(BaseModel):
    id: UUID
    game_role_id: UUID
    override_max_count: int | None = None
    override_min_count: int | None = None


class ApplicationFormFieldResponse(BaseModel):
    id: UUID
    name: str
    is_private: bool
    is_required: bool


class ApplicationFormTimeSettingsResponse(BaseModel):
    start_time: datetime | None = None
    end_time: datetime | None = None


class ApplicationFormSettingsResponse(BaseModel):
    event_id: UUID
    event_name: str
    required_integrations: list[ApplicationFormIntegrationResponse] = Field(default_factory=list)
    available_roles: list[ApplicationFormRoleResponse] = Field(default_factory=list)
    custom_fields: list[ApplicationFormFieldResponse] = Field(default_factory=list)
    time_settings: ApplicationFormTimeSettingsResponse | None = None
