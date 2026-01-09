from uuid import UUID
from faststream.rabbit import RabbitBroker, RabbitMessage

from ..models.roles.request import (
    CreateServerRoleRequest,
    DeleteServerRoleRequest,
    ListServerRolesRequest,
    UpdateServerRolePermissionsRequest,
    UpdateServerRoleRequest,
)

from ..models.request import AccessDataRequest
from src.domain.models.access import AccessData

from ..models.roles.response import PermissionResponse, ServerRoleResponse

from ..models.response import ErrorResponse, ResponseMessage, StatusResponse


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
        self, access: AccessData
    ) -> ResponseMessage[list[ServerRoleResponse] | ErrorResponse]:
        access_data = AccessDataRequest(
            member_id=access.member_id,
            server_id=access.server_id,
            permission_mask=access.permission_mask,
            restriction_mask=access.restriction_mask,
        )
        request = ListServerRolesRequest(access_data=access_data)
        response: RabbitMessage = await self.broker.request(
            request, queue="server.role.list"
        )
        return ResponseMessage[
            list[ServerRoleResponse] | ErrorResponse
        ].model_validate_json(response.body)

    async def create_role(
        self,
        access: AccessData,
        name: str,
        position: int,
    ) -> ResponseMessage[ServerRoleResponse | ErrorResponse]:
        access_data = AccessDataRequest(
            member_id=access.member_id,
            server_id=access.server_id,
            permission_mask=access.permission_mask,
            restriction_mask=access.restriction_mask,
        )
        request = CreateServerRoleRequest(
            access_data=access_data,
            name=name,
            position=position,
        )
        response: RabbitMessage = await self.broker.request(
            request, queue="server.role.create"
        )
        return ResponseMessage[ServerRoleResponse | ErrorResponse].model_validate_json(
            response.body
        )

    async def update_role(
        self,
        access: AccessData,
        role_id: UUID,
        name: str | None = None,
        position: int | None = None,
    ) -> ResponseMessage[ServerRoleResponse | ErrorResponse]:
        access_data = AccessDataRequest(
            member_id=access.member_id,
            server_id=access.server_id,
            permission_mask=access.permission_mask,
            restriction_mask=access.restriction_mask,
        )
        request = UpdateServerRoleRequest(
            access_data=access_data,
            role_id=role_id,
            name=name,
            position=position,
        )
        response: RabbitMessage = await self.broker.request(
            request, queue="server.role.update"
        )
        return ResponseMessage[ServerRoleResponse | ErrorResponse].model_validate_json(
            response.body
        )

    async def update_role_permission(
        self,
        access: AccessData,
        role_id: UUID,
        target_permissions_ids: list[UUID],
    ) -> ResponseMessage[ServerRoleResponse | ErrorResponse]:
        access_data = AccessDataRequest(
            member_id=access.member_id,
            server_id=access.server_id,
            permission_mask=access.permission_mask,
            restriction_mask=access.restriction_mask,
        )
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
        self, access: AccessData, role_id: UUID
    ) -> ResponseMessage[StatusResponse | ErrorResponse]:
        request = DeleteServerRoleRequest(
            access_data=AccessDataRequest(
                member_id=access.member_id,
                server_id=access.server_id,
                permission_mask=access.permission_mask,
                restriction_mask=access.restriction_mask,
            ),
            role_id=role_id,
        )
        response: RabbitMessage = await self.broker.request(
            request, queue="server.role.delete"
        )
        return ResponseMessage[StatusResponse | ErrorResponse].model_validate_json(
            response.body
        )
