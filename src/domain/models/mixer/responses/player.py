from uuid import UUID

from pydantic import BaseModel, Field

from src.domain.models.server.custom.response import CustomResponse
from src.domain.models.server.member.response import ReducedMemberResponse

from ..enums import EventPlayerStatus


class PlayerRoleResponse(BaseModel):
    game_role_id: UUID
    priority: int


class EventPlayerResponse(BaseModel):
    id: UUID
    member: ReducedMemberResponse
    status: EventPlayerStatus
    is_draft_pinned: bool
    application_id: UUID | None = None
    custom: CustomResponse | None = None
    roles: list[PlayerRoleResponse] = Field(default_factory=list)


class PlayerUpdateResultResponse(BaseModel):
    id: UUID
    member: ReducedMemberResponse
    status: EventPlayerStatus
    custom: CustomResponse | None = None
