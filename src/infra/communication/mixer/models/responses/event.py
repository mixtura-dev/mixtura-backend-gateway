from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from ..enums import EventMatchType, EventStatus, TeamFormation


class OrganizerData(BaseModel):
    id: UUID
    member_id: UUID


class OrganizerItem(BaseModel):
    id: UUID
    event_id: UUID
    member_id: UUID


class RequiredIntegrationData(BaseModel):
    id: UUID
    provider_id: UUID


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
