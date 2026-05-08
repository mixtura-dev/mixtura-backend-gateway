from uuid import UUID


async def get_access(server_id: UUID, user_id: UUID, member_service):
    return await member_service.get_member_by_user(server_id, user_id)
