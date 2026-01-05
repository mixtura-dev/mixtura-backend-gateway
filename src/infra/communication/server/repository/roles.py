from uuid import UUID
from faststream.rabbit import RabbitBroker, RabbitMessage

from ..schemas.roles.request import (
    CreateServerRoleRequest,
    DeleteServerRoleRequest,
    ListServerRolesRequest,
    UpdateServerRolePermissionsRequest,
    UpdateServerRoleRequest,
)

from ..schemas.request import AccessDataRequest

from ..schemas.roles.response import PermissionResponse, ServerRoleResponse

from ..schemas.response import ErrorResponse, ResponseMessage, StatusResponse


class ServerRoleRepository:
    def __init__(self, broker: RabbitBroker):
        self.broker = broker

    async def get_global_permissions(
        self,
    ) -> ResponseMessage[list[PermissionResponse] | ErrorResponse]:
        response: RabbitMessage = await self.broker.request(
            None, queue="server.global.permissions"
        )
        return ResponseMessage[
            list[PermissionResponse] | ErrorResponse
        ].model_validate_json(response.body)

    async def list_roles(
        self, access_data: AccessDataRequest
    ) -> ResponseMessage[list[ServerRoleResponse] | ErrorResponse]:
        request = ListServerRolesRequest(access_data=access_data)
        response: RabbitMessage = await self.broker.request(
            request, queue="server.role.list"
        )
        return ResponseMessage[
            list[ServerRoleResponse] | ErrorResponse
        ].model_validate_json(response.body)

    async def create_role(
        self,
        access_data: AccessDataRequest,
        name: str,
        position: int,
        permission_mask: int,
    ) -> ResponseMessage[ServerRoleResponse | ErrorResponse]:
        request = CreateServerRoleRequest(
            access_data=access_data,
            name=name,
            position=position,
            permission_mask=permission_mask,
        )
        response: RabbitMessage = await self.broker.request(
            request, queue="server.role.create"
        )
        return ResponseMessage[ServerRoleResponse | ErrorResponse].model_validate_json(
            response.body
        )

    async def update_role(
        self,
        access_data: AccessDataRequest,
        role_id: UUID,
        target_permissions_ids: list[UUID],
        name: str | None = None,
        position: int | None = None,
    ) -> ResponseMessage[ServerRoleResponse | ErrorResponse]:
        request = UpdateServerRoleRequest(
            access_data=access_data,
            role_id=role_id,
            name=name,
            position=position,
            target_permissions_ids=target_permissions_ids,
        )
        response: RabbitMessage = await self.broker.request(
            request, queue="server.role.update"
        )
        return ResponseMessage[ServerRoleResponse | ErrorResponse].model_validate_json(
            response.body
        )

    async def update_role_permission(
        self,
        access_data: AccessDataRequest,
        role_id: UUID,
        target_permissions_ids: list[UUID],
    ) -> ResponseMessage[ServerRoleResponse | ErrorResponse]:
        request = UpdateServerRolePermissionsRequest(
            access_data=access_data,
            role_id=role_id,
            target_permissions_ids=target_permissions_ids,
        )
        response: RabbitMessage = await self.broker.request(
            request, queue="server.role.permissions.update"
        )
        return ResponseMessage[ServerRoleResponse | ErrorResponse].model_validate_json(
            response.body
        )

    async def delete_role(
        self, access_data: AccessDataRequest, role_id: UUID
    ) -> ResponseMessage[StatusResponse | ErrorResponse]:
        request = DeleteServerRoleRequest(access_data=access_data, role_id=role_id)
        response: RabbitMessage = await self.broker.request(
            request, queue="server.role.delete"
        )
        return ResponseMessage[StatusResponse | ErrorResponse].model_validate_json(
            response.body
        )
