from uuid import UUID

from pydantic import BaseModel

from ..shared import AccessDataRequest, PaginationRequest


class ListOrganizersRequest(BaseModel):
    event_id: UUID
    access_data: AccessDataRequest
    pagination: PaginationRequest = PaginationRequest()


class AddOrganizerRequest(BaseModel):
    access_data: AccessDataRequest
    event_id: UUID
    member_id: UUID


class RemoveOrganizerRequest(AddOrganizerRequest):
    pass
