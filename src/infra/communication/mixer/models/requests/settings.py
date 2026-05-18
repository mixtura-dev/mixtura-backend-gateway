from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from ..shared import AccessDataRequest


class AddIntegrationRequest(BaseModel):
    access_data: AccessDataRequest
    event_id: UUID
    name: str


class RemoveIntegrationRequest(BaseModel):
    access_data: AccessDataRequest
    event_id: UUID
    integration_id: UUID


class AddGameRoleRequest(BaseModel):
    access_data: AccessDataRequest
    event_id: UUID
    game_role_id: UUID
    override_max_count: int | None = None
    override_min_count: int | None = None


class UpdateGameRoleRequest(BaseModel):
    access_data: AccessDataRequest
    event_id: UUID
    selected_role_id: UUID
    override_max_count: int | None = None
    override_min_count: int | None = None


class RemoveGameRoleRequest(BaseModel):
    access_data: AccessDataRequest
    event_id: UUID
    selected_role_id: UUID


class AddCustomFieldRequest(BaseModel):
    access_data: AccessDataRequest
    event_id: UUID
    name: str
    is_private: bool = False
    is_required: bool = False


class UpdateCustomFieldRequest(BaseModel):
    access_data: AccessDataRequest
    event_id: UUID
    field_id: UUID
    name: str | None = None
    is_private: bool | None = None
    is_required: bool | None = None


class RemoveCustomFieldRequest(BaseModel):
    access_data: AccessDataRequest
    event_id: UUID
    field_id: UUID


class UpdateTimeSettingsRequest(BaseModel):
    access_data: AccessDataRequest
    event_id: UUID
    start_time: datetime | None = None
    end_time: datetime | None = None
