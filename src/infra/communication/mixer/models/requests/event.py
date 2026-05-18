from uuid import UUID

from pydantic import BaseModel

from ..enums import EventMatchType, TeamFormation
from ..shared import AccessDataRequest


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


class ListEventsUnifiedRequest(BaseModel):
    server_id: UUID
    access_data: AccessDataRequest
