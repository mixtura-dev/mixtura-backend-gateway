from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from .event import (
    ApplicationCustomFieldResponse,
    ApplicationTimeSettingsResponse,
    RequiredIntegrationResponse,
    SelectedGameRoleResponse,
)
from ..enums import ApplicationStatus


class SubmitApplicationResponse(BaseModel):
    id: UUID
    status: ApplicationStatus
    auto_approved: bool
    player_id: UUID


class ApplicationRoleItemResponse(BaseModel):
    role_id: UUID
    game_role_id: UUID | None = None
    priority: int


class ApplicationIntegrationItemResponse(BaseModel):
    integration_id: UUID
    provider_id: UUID
    provider_name: str
    account_name: str | None = None


class ApplicationListItemUserResponse(BaseModel):
    id: UUID
    username: str | None = None


class ApplicationListItemResponse(BaseModel):
    id: UUID
    member_id: UUID
    status: ApplicationStatus
    created_at: datetime
    user: ApplicationListItemUserResponse | None = None
    roles: list[ApplicationRoleItemResponse] = []
    integrations: list[ApplicationIntegrationItemResponse] = []


class ApplicationFilledFieldResponse(BaseModel):
    custom_field_id: UUID
    value: str


class ApplicationRolePriorityResponse(BaseModel):
    role_id: UUID
    priority: int


class ApplicationIntegrationResponse(BaseModel):
    integration_id: UUID
    provider_id: UUID
    provider_name: str


class ApplicationDetailResponse(BaseModel):
    id: UUID
    event_id: UUID
    member_id: UUID
    status: ApplicationStatus
    role_priorities: list[ApplicationRolePriorityResponse] = Field(default_factory=list)
    filled_fields: list[ApplicationFilledFieldResponse] = Field(default_factory=list)
    integrations: list[ApplicationIntegrationResponse] = Field(default_factory=list)
    event_player_id: UUID | None = None


class ReviewApplicationResponse(BaseModel):
    id: UUID
    status: ApplicationStatus
    player_id: UUID | None = None


class ApplicationFormSettingsResponse(BaseModel):
    event_id: UUID
    event_name: str
    required_integrations: list[RequiredIntegrationResponse] = Field(default_factory=list)
    available_roles: list[SelectedGameRoleResponse] = Field(default_factory=list)
    custom_fields: list[ApplicationCustomFieldResponse] = Field(default_factory=list)
    time_settings: ApplicationTimeSettingsResponse | None = None
