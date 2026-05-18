from uuid import UUID

from pydantic import BaseModel

from ..shared import AccessDataRequest, PaginationRequest


class ListTeamsRequest(BaseModel):
    event_id: UUID
    access_data: AccessDataRequest
    pagination: PaginationRequest = PaginationRequest()
