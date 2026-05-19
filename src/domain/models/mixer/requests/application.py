from uuid import UUID

from pydantic import BaseModel, Field, field_validator

from ..enums import ApplicationStatus


class IntegrationPayload(BaseModel):
    integration_id: UUID


class FilledFieldPayload(BaseModel):
    custom_field_id: UUID
    value: str


class RolePriorityPayload(BaseModel):
    role_id: UUID
    priority: int


class SubmitApplicationRequest(BaseModel):
    integrations: list[IntegrationPayload] = Field(default_factory=list)
    filled_fields: list[FilledFieldPayload] = Field(default_factory=list)
    role_priorities: list[RolePriorityPayload] = Field(default_factory=list)

    @field_validator("filled_fields", mode="before")
    @classmethod
    def _convert_filled_fields_map(cls, value):
        if isinstance(value, dict):
            return [
                {"custom_field_id": custom_field_id, "value": field_value}
                for custom_field_id, field_value in value.items()
            ]
        return value

    @field_validator("role_priorities", mode="before")
    @classmethod
    def _convert_role_priorities_map(cls, value):
        if isinstance(value, dict):
            return [
                {"role_id": role_id, "priority": priority}
                for role_id, priority in value.items()
            ]
        return value


class ReviewApplicationRequest(BaseModel):
    status: ApplicationStatus
    role_priorities: list[RolePriorityPayload] = Field(default_factory=list)

    @field_validator("role_priorities", mode="before")
    @classmethod
    def _convert_role_priorities_map(cls, value):
        if isinstance(value, dict):
            return [
                {"role_id": role_id, "priority": priority}
                for role_id, priority in value.items()
            ]
        return value
