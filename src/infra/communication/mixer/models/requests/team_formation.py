from uuid import UUID

from pydantic import BaseModel, Field

from ..shared import AccessDataRequest, PaginationRequest


class RatingSnapshotInput(BaseModel):
    member_id: UUID
    event_player_id: UUID | None = None
    game_role_id: UUID
    priority: int = 1
    open_rating: float


class RunTeamFormationRequest(BaseModel):
    access_data: AccessDataRequest
    draft_id: UUID
    use_effective_rating: bool = False
    rating_snapshot: list[RatingSnapshotInput] = Field(default_factory=list)
    rating_settings: dict[str, str | int | float | bool | None] | None = None
    team_count: int | None = None


class GetTeamFormationRequest(BaseModel):
    draft_id: UUID
    access_data: AccessDataRequest
    pagination: PaginationRequest = PaginationRequest()


class ChooseTeamFormationVariantRequest(BaseModel):
    access_data: AccessDataRequest
    draft_id: UUID
    variant_id: UUID
