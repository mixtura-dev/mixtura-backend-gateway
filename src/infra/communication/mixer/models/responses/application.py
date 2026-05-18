from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from ..enums import ApplicationStatus
from .event import (
    ApplicationCustomFieldData,
    ApplicationTimeSettingsData,
    RequiredIntegrationData,
    SelectedGameRoleData,
)


class ApplicationRoleItem(BaseModel):
    role_id: UUID
    game_role_id: UUID | None = None
    priority: int


class ApplicationIntegrationItem(BaseModel):
    integration_id: UUID
    provider_id: UUID
    provider_name: str


class ApplicationFilledFieldItem(BaseModel):
    custom_field_id: UUID
    value: str


class ApplicationRolePriorityItem(BaseModel):
    role_id: UUID
    priority: int


class ApplicationSubmitResult(BaseModel):
    id: UUID
    status: ApplicationStatus
    auto_approved: bool
    player_id: UUID


class ApplicationReviewResult(BaseModel):
    id: UUID
    status: ApplicationStatus
    player_id: UUID | None = None


class ApplicationDetail(BaseModel):
    id: UUID
    event_id: UUID
    member_id: UUID
    status: ApplicationStatus
    role_priorities: list[ApplicationRolePriorityItem] = Field(default_factory=list)
    filled_fields: list[ApplicationFilledFieldItem] = Field(default_factory=list)
    integrations: list[ApplicationIntegrationItem] = Field(default_factory=list)
    event_player_id: UUID | None = None


class ApplicationListItem(BaseModel):
    id: UUID
    member_id: UUID
    status: ApplicationStatus
    created_at: datetime
    roles: list[ApplicationRoleItem] = Field(default_factory=list)
    integrations: list[ApplicationIntegrationItem] = Field(default_factory=list)


class ApplicationFormSettings(BaseModel):
    event_id: UUID
    event_name: str
    required_integrations: list[RequiredIntegrationData] = Field(default_factory=list)
    available_roles: list[SelectedGameRoleData] = Field(default_factory=list)
    custom_fields: list[ApplicationCustomFieldData] = Field(default_factory=list)
    time_settings: ApplicationTimeSettingsData | None = None
