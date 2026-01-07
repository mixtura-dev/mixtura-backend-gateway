from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict


# class ServerPermissionResponse(BaseModel):
#     model_config = ConfigDict(from_attributes=True)
#
#     id: UUID
#     code_name: str


class ServerRoleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    position: int
    permission_mask: int


class ReducedMemberResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    nickname: str
    user_id: UUID | None


class MemberResponse(ReducedMemberResponse):
    model_config = ConfigDict(from_attributes=True)

    server_id: UUID
    joined_at: datetime
    server_role: ServerRoleResponse | None


class RestrictionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    code: str


class MemberRestrictionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    reason: str
    expiration_date: datetime
    restriction: RestrictionResponse
