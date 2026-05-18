from uuid import UUID

from pydantic import BaseModel

from ..enums import EventPlayerStatus
from ..shared import AccessDataRequest, PaginationRequest


class RolePriorityInput(BaseModel):
    game_role_id: UUID
    priority: int


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
    custom_id: UUID | None = None


class RemovePlayerRequest(BaseModel):
    access_data: AccessDataRequest
    event_id: UUID
    member_id: UUID


class AddPlayerRequest(BaseModel):
    access_data: AccessDataRequest
    event_id: UUID
    member_id: UUID
    application_id: UUID | None = None
    custom_id: UUID | None = None
    is_draft_pinned: bool = False
    roles: list[RolePriorityInput] | None = None


class UpdatePlayerRolesRequest(BaseModel):
    access_data: AccessDataRequest
    event_id: UUID
    member_id: UUID
    roles: list[RolePriorityInput]
