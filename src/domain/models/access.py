from uuid import UUID
from pydantic import BaseModel


class AccessData(BaseModel):
    user_id: UUID
    member_id: UUID | None
    server_id: UUID
    permission_mask: int = 0
    restriction_mask: int = 0
