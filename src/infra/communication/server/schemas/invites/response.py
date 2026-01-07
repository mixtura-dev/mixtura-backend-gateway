from uuid import UUID
from pydantic import BaseModel, ConfigDict

from ..member.response import MemberResponse, ReducedMemberResponse

from ..core.response import ServerListResponse


class InviteAdminResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    key: str
    inviter: MemberResponse
    use_limit: int

class InviteKeyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    inviter: ReducedMemberResponse
    server: ServerListResponse