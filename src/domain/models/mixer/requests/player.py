from uuid import UUID

from pydantic import BaseModel

from ..enums import EventPlayerStatus


class PlayerRolePayload(BaseModel):
    game_role_id: UUID
    priority: int


class UpdatePlayerStatusRequest(BaseModel):
    status: EventPlayerStatus
    custom_id: UUID | None = None


class AddPlayerRequest(BaseModel):
    member_id: UUID
    application_id: UUID | None = None
    custom_id: UUID | None = None
    is_draft_pinned: bool = False
    roles: list[PlayerRolePayload] | None = None


class UpdatePlayerRolesRequest(BaseModel):
    roles: list[PlayerRolePayload]
