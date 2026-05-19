from uuid import UUID

from pydantic import BaseModel

from ..enums import EventPlayerStatus


class CreateDraftRequest(BaseModel):
    player_ids: list[UUID] | None = None
    statuses: list[EventPlayerStatus] | None = None
    limit: int | None = None
    pinned_only: bool = False
