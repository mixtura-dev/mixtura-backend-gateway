from uuid import UUID

from pydantic import BaseModel


class RunTeamFormationRequest(BaseModel):
    use_effective_rating: bool = False
    rating_settings: dict[str, str | int | float | bool | None] | None = None
    team_count: int | None = None
