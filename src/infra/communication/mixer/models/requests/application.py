from uuid import UUID

from pydantic import BaseModel, Field

from ..enums import ApplicationStatus
from ..shared import AccessDataRequest, PaginationRequest


class IntegrationPayload(BaseModel):
    integration_id: UUID
    provider_id: UUID
    provider_name: str


class FilledFieldPayload(BaseModel):
    custom_field_id: UUID
    value: str


class RolePriorityPayload(BaseModel):
    role_id: UUID
    priority: int


class SubmitApplicationRequest(BaseModel):
    access_data: AccessDataRequest
    event_id: UUID
    integrations: list[IntegrationPayload] = Field(default_factory=list)
    filled_fields: list[FilledFieldPayload] = Field(default_factory=list)
    role_priorities: list[RolePriorityPayload] = Field(default_factory=list)


class GetApplicationRequest(BaseModel):
    application_id: UUID
    access_data: AccessDataRequest


class ReviewApplicationRequest(BaseModel):
    access_data: AccessDataRequest
    application_id: UUID
    status: ApplicationStatus
    role_priorities: list[RolePriorityPayload] = Field(default_factory=list)


class ListApplicationsRequest(BaseModel):
    event_id: UUID
    access_data: AccessDataRequest
    status: ApplicationStatus | None = None
    pagination: PaginationRequest = PaginationRequest()
    sort_by: str = "created_at"
    sort_order: str = "desc"


class GetApplicationFormSettingsRequest(BaseModel):
    event_id: UUID
    access_data: AccessDataRequest
