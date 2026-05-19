from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from src.domain.models.server.member.response import ReducedMemberResponse

from ..enums import EventMatchType, EventStatus, TeamFormation


class OrganizerResponse(BaseModel):
    id: UUID
    member_id: UUID


class OrganizerListItemResponse(BaseModel):
    member: ReducedMemberResponse


class OrganizerItemResponse(BaseModel):
    id: UUID
    event_id: UUID
    member_id: UUID


class RequiredIntegrationResponse(BaseModel):
    id: UUID
    provider_id: UUID


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
