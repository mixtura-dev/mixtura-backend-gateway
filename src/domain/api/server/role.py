from uuid import UUID
from fastapi_controllers import Controller, delete, get, patch, post, put

from ...models.server.roles.request import (
    CreateServerRoleRequest,
    UpdateRolePermissionsRequest,
    UpdateServerRoleRequest,
)

from ...models.response import StatusResponse

from ...models.server.member.response import ServerRoleResponse

from ....dependency import (
    AuthorizedUserID,
    MemberServiceDependency,
    ServerRoleServiceDependency,
)


class ServerRoleController(Controller):
    prefix = "/{server_id}/role"
    tags = ["Server roles"]

    def __init__(self, user_id: AuthorizedUserID) -> None:
        self.user_id = user_id

    @get("/", response_model=list[ServerRoleResponse])
    async def list_server_roles(
        self,
        server_id: UUID,
        member_service: MemberServiceDependency,
        server_role_service: ServerRoleServiceDependency,
    ):
        access = await member_service.get_member_by_user(server_id, self.user_id)
        roles = await server_role_service.list_roles(access)
        return roles

    @post("/", response_model=ServerRoleResponse)
    async def create_server_role(
        self,
        server_id: UUID,
        body: CreateServerRoleRequest,
        member_service: MemberServiceDependency,
        server_role_service: ServerRoleServiceDependency,
    ):
        access = await member_service.get_member_by_user(server_id, self.user_id)
        role = await server_role_service.create_role(
            access, body.name, body.position
        )
        return role

    @patch("/{role_id}", response_model=ServerRoleResponse)
    async def update_server_role(
        self,
        server_id: UUID,
        role_id: UUID,
        body: UpdateServerRoleRequest,
        member_service: MemberServiceDependency,
        server_role_service: ServerRoleServiceDependency,
    ):
        access = await member_service.get_member_by_user(server_id, self.user_id)
        role = await server_role_service.update_role(
            access,
            role_id,
            body.name,
            body.position,
        )
        return role
    
    @put("/{role_id}/permissions", response_model=ServerRoleResponse)
    async def update_server_role_permissions(
        self,
        server_id: UUID,
        role_id: UUID,
        body: UpdateRolePermissionsRequest,
        member_service: MemberServiceDependency,
        server_role_service: ServerRoleServiceDependency,
    ):
        access = await member_service.get_member_by_user(server_id, self.user_id)
        role = await server_role_service.update_role_permission(
            access,
            role_id,
            body.permissions_ids,
        )
        return role

    @delete("/{role_id}", response_model=StatusResponse)
    async def delete_server_role(
        self,
        server_id: UUID,
        role_id: UUID,
        member_service: MemberServiceDependency,
        server_role_service: ServerRoleServiceDependency,
    ):
        access = await member_service.get_member_by_user(server_id, self.user_id)
        await server_role_service.delete_role(access, role_id)
        return StatusResponse()
