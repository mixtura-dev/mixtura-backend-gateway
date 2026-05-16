from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class EventMatchType(str, Enum):
    SINGLE = "SINGLE"
    TOURNAMENT = "TOURNAMENT"


class TeamFormation(str, Enum):
    DRAFT = "DRAFT"
    BALANCE = "BALANCE"
    MANUAL = "MANUAL"


class ApplicationStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    WAITLIST = "WAITLIST"


class EventPlayerStatus(str, Enum):
    REGISTERED = "REGISTERED"
    SELECTED = "SELECTED"
    PLAYING = "PLAYING"
    COMPLETED = "COMPLETED"
    BENCHED = "BENCHED"


class CreateEventRequest(BaseModel):
    name: str
    match_type: EventMatchType
    use_application: bool
    is_public: bool
    team_size: int
    team_formation: TeamFormation
    allow_multiple_drafts: bool


class UpdateEventRequest(BaseModel):
    name: str | None = None
    match_type: EventMatchType | None = None
    use_application: bool | None = None
    is_public: bool | None = None
    team_size: int | None = None
    team_formation: TeamFormation | None = None
    allow_multiple_drafts: bool | None = None


class AddOrganizerRequest(BaseModel):
    member_id: UUID


class IntegrationPayload(BaseModel):
    integration_id: UUID


class FilledFieldPayload(BaseModel):
    custom_field_id: UUID
    value: str


class RolePriorityPayload(BaseModel):
    role_id: UUID
    priority: int


class SubmitApplicationRequest(BaseModel):
    integrations: list[IntegrationPayload] = Field(default_factory=list)
    filled_fields: list[FilledFieldPayload] = Field(default_factory=list)
    role_priorities: list[RolePriorityPayload] = Field(default_factory=list)

    @field_validator("filled_fields", mode="before")
    @classmethod
    def _convert_filled_fields_map(cls, value):
        if isinstance(value, dict):
            return [
                {"custom_field_id": custom_field_id, "value": field_value}
                for custom_field_id, field_value in value.items()
            ]
        return value

    @field_validator("role_priorities", mode="before")
    @classmethod
    def _convert_role_priorities_map(cls, value):
        if isinstance(value, dict):
            return [
                {"role_id": role_id, "priority": priority}
                for role_id, priority in value.items()
            ]
        return value


class ReviewApplicationRequest(BaseModel):
    status: ApplicationStatus
    role_priorities: list[RolePriorityPayload] = Field(default_factory=list)

    @field_validator("role_priorities", mode="before")
    @classmethod
    def _convert_role_priorities_map(cls, value):
        if isinstance(value, dict):
            return [
                {"role_id": role_id, "priority": priority}
                for role_id, priority in value.items()
            ]
        return value


class UpdatePlayerStatusRequest(BaseModel):
    status: EventPlayerStatus
    custom_id: UUID | None = None


class CreateDraftRequest(BaseModel):
    player_ids: list[UUID] | None = None
    statuses: list[EventPlayerStatus] | None = None
    limit: int | None = None
    pinned_only: bool = False


class RatingSnapshotInput(BaseModel):
    member_id: UUID
    event_player_id: UUID | None = None
    game_role_id: UUID
    priority: int = 1
    open_rating: float


class RunTeamFormationRequest(BaseModel):
    use_effective_rating: bool = False
    rating_snapshot: list[RatingSnapshotInput] = Field(default_factory=list)
    rating_settings: dict[str, str | int | float | bool | None] | None = None
    team_count: int | None = None


class SetupMatchRequest(BaseModel):
    team_ids: list[UUID]
    draft_id: UUID | None = None
    scheduled_at: datetime | None = None


class RecordMatchResultRequest(BaseModel):
    scores: dict[UUID, int]
    winner_id: UUID | None = None
    is_draw: bool = False
    forfeit_team_ids: list[UUID] = Field(default_factory=list)
    rating_settings: dict[str, str | int | float | bool | None] | None = None


class AddIntegrationRequest(BaseModel):
    name: str


class AddGameRoleRequest(BaseModel):
    game_role_id: UUID
    override_max_count: int | None = None
    override_min_count: int | None = None


class UpdateGameRoleRequest(BaseModel):
    override_max_count: int | None = None
    override_min_count: int | None = None


class AddCustomFieldRequest(BaseModel):
    name: str
    is_private: bool = False
    is_required: bool = False


class UpdateCustomFieldRequest(BaseModel):
    name: str | None = None
    is_private: bool | None = None
    is_required: bool | None = None


class UpdateTimeSettingsRequest(BaseModel):
    start_time: datetime | None = None
    end_time: datetime | None = None
