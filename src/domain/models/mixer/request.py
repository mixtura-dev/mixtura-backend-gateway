from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


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
    rating_set_id: UUID | None = None


class UpdateEventRequest(BaseModel):
    name: str | None = None
    match_type: EventMatchType | None = None
    use_application: bool | None = None
    is_public: bool | None = None
    team_size: int | None = None
    team_formation: TeamFormation | None = None
    allow_multiple_drafts: bool | None = None
    rating_set_id: UUID | None = None


class AddOrganizerRequest(BaseModel):
    member_id: UUID


class SubmitApplicationRequest(BaseModel):
    integration_ids: list[UUID] = Field(default_factory=list)
    filled_fields: dict[UUID, str] = Field(default_factory=dict)
    role_priorities: dict[UUID, int] = Field(default_factory=dict)


class ReviewApplicationRequest(BaseModel):
    status: ApplicationStatus


class UpdatePlayerStatusRequest(BaseModel):
    status: EventPlayerStatus


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
