from uuid import UUID

from pydantic import BaseModel, Field

from ..enums import EventPlayerStatus


class PlayerRoleItem(BaseModel):
    game_role_id: UUID
    priority: int


class PlayerItem(BaseModel):
    id: UUID
    member_id: UUID
    status: EventPlayerStatus
    is_draft_pinned: bool
    application_id: UUID | None = None
    custom_id: UUID | None = None
    roles: list[PlayerRoleItem] = Field(default_factory=list)


class PlayerUpdateResult(BaseModel):
    id: UUID
    member_id: UUID
    status: EventPlayerStatus
    custom_id: UUID | None = None
