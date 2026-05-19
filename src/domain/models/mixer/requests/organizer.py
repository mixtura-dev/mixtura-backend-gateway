from uuid import UUID

from pydantic import BaseModel


class AddOrganizerRequest(BaseModel):
    member_id: UUID
