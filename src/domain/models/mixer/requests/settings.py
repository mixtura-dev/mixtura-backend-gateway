from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class AddIntegrationRequest(BaseModel):
    name: str


class AddGameRoleRequest(BaseModel):
    game_role_id: UUID
    override_max_count: int | None = None
    override_min_count: int | None = None


class UpdateGameRoleRequest(BaseModel):
    override_max_count: int | None = None
    override_min_count: int | None = None


class AddCustomFieldRequest(BaseModel):
    name: str
    is_private: bool = False
    is_required: bool = False


class UpdateCustomFieldRequest(BaseModel):
    name: str | None = None
    is_private: bool | None = None
    is_required: bool | None = None


class UpdateTimeSettingsRequest(BaseModel):
    start_time: datetime | None = None
    end_time: datetime | None = None
