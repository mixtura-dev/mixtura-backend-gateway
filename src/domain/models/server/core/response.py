from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict

from ..game_roles.response import GameRoleSetResponse
from ..games.response import GameResponse
from ..rating.response import RatingSetResponse


class ServerListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    description: str
    icon_url: None | str = None
    banner_url: None | str = None
    owner_id: UUID
    public: bool
    created_at: datetime


class ServerDetailResponse(ServerListResponse):
    rating_set: Optional[RatingSetResponse] = None
    role_set: Optional[GameRoleSetResponse] = None

    games: list[GameResponse] = []
