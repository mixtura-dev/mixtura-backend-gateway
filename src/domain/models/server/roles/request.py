from uuid import UUID
from pydantic import BaseModel, ConfigDict


class UpdateServerRoleRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str | None
    position: int | None


class UpdateRolePermissionsRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    permissions_ids: list[UUID]


class CreateServerRoleRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    position: int
