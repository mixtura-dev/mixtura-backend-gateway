from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class AccessDataRequest(BaseModel):
    member_id: UUID | None
    server_id: UUID
    permission_mask: int
    restriction_mask: int


class PaginationRequest(BaseModel):
    page: int | None = None
    page_size: int = 50


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
    access_data: AccessDataRequest
    name: str
    match_type: EventMatchType
    use_application: bool
    is_public: bool
    team_size: int
    team_formation: TeamFormation
    allow_multiple_drafts: bool
    rating_set_id: UUID | None = None


class GetEventRequest(BaseModel):
    event_id: UUID
    access_data: AccessDataRequest


class ListEventsRequest(BaseModel):
    server_id: UUID | None = None
    access_data: AccessDataRequest
    pagination: PaginationRequest = PaginationRequest()


class UpdateEventRequest(BaseModel):
    access_data: AccessDataRequest
    event_id: UUID
    name: str | None = None
    match_type: EventMatchType | None = None
    use_application: bool | None = None
    is_public: bool | None = None
    team_size: int | None = None
    team_formation: TeamFormation | None = None
    allow_multiple_drafts: bool | None = None
    rating_set_id: UUID | None = None


class ActivateEventRequest(BaseModel):
    access_data: AccessDataRequest
    event_id: UUID


class OpenRegistrationRequest(ActivateEventRequest):
    pass


class CloseRegistrationRequest(ActivateEventRequest):
    pass


class CancelEventRequest(ActivateEventRequest):
    pass


class CompleteEventRequest(ActivateEventRequest):
    pass


class ListOrganizersRequest(BaseModel):
    event_id: UUID
    access_data: AccessDataRequest
    pagination: PaginationRequest = PaginationRequest()


class AddOrganizerRequest(BaseModel):
    access_data: AccessDataRequest
    event_id: UUID
    member_id: UUID


class RemoveOrganizerRequest(AddOrganizerRequest):
    pass


class SubmitApplicationRequest(BaseModel):
    access_data: AccessDataRequest
    event_id: UUID
    integration_ids: list[UUID] = Field(default_factory=list)
    filled_fields: dict[UUID, str] = Field(default_factory=dict)
    role_priorities: dict[UUID, int] = Field(default_factory=dict)


class GetApplicationRequest(BaseModel):
    application_id: UUID
    access_data: AccessDataRequest


class ReviewApplicationRequest(BaseModel):
    access_data: AccessDataRequest
    application_id: UUID
    status: ApplicationStatus


class ListApplicationsRequest(BaseModel):
    event_id: UUID
    access_data: AccessDataRequest
    status: ApplicationStatus | None = None
    pagination: PaginationRequest = PaginationRequest()


class ListPlayersRequest(BaseModel):
    event_id: UUID
    access_data: AccessDataRequest
    status: EventPlayerStatus | None = None
    pagination: PaginationRequest = PaginationRequest()


class UpdatePlayerStatusRequest(BaseModel):
    access_data: AccessDataRequest
    event_id: UUID
    member_id: UUID
    status: EventPlayerStatus


class RemovePlayerRequest(BaseModel):
    access_data: AccessDataRequest
    event_id: UUID
    member_id: UUID


class CreateDraftRequest(BaseModel):
    access_data: AccessDataRequest
    event_id: UUID
    player_ids: list[UUID] | None = None
    statuses: list[EventPlayerStatus] | None = None
    limit: int | None = None
    pinned_only: bool = False


class GetDraftRequest(BaseModel):
    draft_id: UUID
    access_data: AccessDataRequest


class ListDraftsRequest(BaseModel):
    event_id: UUID
    access_data: AccessDataRequest
    pagination: PaginationRequest = PaginationRequest()


class RatingSnapshotInput(BaseModel):
    member_id: UUID
    event_player_id: UUID | None = None
    game_role_id: UUID
    priority: int = 1
    open_rating: float


class RunTeamFormationRequest(BaseModel):
    access_data: AccessDataRequest
    draft_id: UUID
    use_effective_rating: bool = False
    rating_snapshot: list[RatingSnapshotInput] = Field(default_factory=list)
    rating_settings: dict[str, str | int | float | bool | None] | None = None
    team_count: int | None = None


class GetTeamFormationRequest(BaseModel):
    draft_id: UUID
    access_data: AccessDataRequest
    pagination: PaginationRequest = PaginationRequest()


class ChooseTeamFormationVariantRequest(BaseModel):
    access_data: AccessDataRequest
    draft_id: UUID
    variant_id: UUID


class ListTeamsRequest(BaseModel):
    event_id: UUID
    access_data: AccessDataRequest
    pagination: PaginationRequest = PaginationRequest()


class SetupMatchRequest(BaseModel):
    access_data: AccessDataRequest
    event_id: UUID
    team_ids: list[UUID]
    draft_id: UUID | None = None
    scheduled_at: datetime | None = None


class RecordMatchResultRequest(BaseModel):
    access_data: AccessDataRequest
    match_id: UUID
    scores: dict[UUID, int]
    winner_id: UUID | None = None
    is_draw: bool = False
    forfeit_team_ids: list[UUID] = Field(default_factory=list)
    rating_settings: dict[str, str | int | float | bool | None] | None = None


class GetMatchRequest(BaseModel):
    match_id: UUID
    access_data: AccessDataRequest


class ListMatchesRequest(BaseModel):
    event_id: UUID
    access_data: AccessDataRequest
    active: bool | None = None
    pagination: PaginationRequest = PaginationRequest()


class HealthRequest(BaseModel):
    pass


class AddIntegrationRequest(BaseModel):
    access_data: AccessDataRequest
    event_id: UUID
    name: str


class RemoveIntegrationRequest(BaseModel):
    access_data: AccessDataRequest
    event_id: UUID
    integration_id: UUID


class AddGameRoleRequest(BaseModel):
    access_data: AccessDataRequest
    event_id: UUID
    game_role_id: UUID
    override_max_count: int | None = None
    override_min_count: int | None = None


class UpdateGameRoleRequest(BaseModel):
    access_data: AccessDataRequest
    event_id: UUID
    selected_role_id: UUID
    override_max_count: int | None = None
    override_min_count: int | None = None


class RemoveGameRoleRequest(BaseModel):
    access_data: AccessDataRequest
    event_id: UUID
    selected_role_id: UUID


class AddCustomFieldRequest(BaseModel):
    access_data: AccessDataRequest
    event_id: UUID
    name: str
    is_private: bool = False
    is_required: bool = False


class UpdateCustomFieldRequest(BaseModel):
    access_data: AccessDataRequest
    event_id: UUID
    field_id: UUID
    name: str | None = None
    is_private: bool | None = None
    is_required: bool | None = None


class RemoveCustomFieldRequest(BaseModel):
    access_data: AccessDataRequest
    event_id: UUID
    field_id: UUID


class UpdateTimeSettingsRequest(BaseModel):
    access_data: AccessDataRequest
    event_id: UUID
    start_time: datetime | None = None
    end_time: datetime | None = None


class ListEventsUnifiedRequest(BaseModel):
    server_id: UUID
    access_data: AccessDataRequest


class GetApplicationFormSettingsRequest(BaseModel):
    event_id: UUID
    access_data: AccessDataRequest
