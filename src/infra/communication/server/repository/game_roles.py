from uuid import UUID
from faststream.rabbit import RabbitBroker, RabbitMessage

from src.infra.communication.rpc import rpc_request
from ..models.game_roles.request import (
    GameRoleItemCreateRequest,
    GameRoleItemDeleteRequest,
    GameRoleItemUpdateRequest,
    GameRoleSetUpdateRequest,
    GetServerGameRoleSetsRequest,
)
from ..models.request import AccessDataRequest
from src.domain.models.access import AccessData
from ..models.game_roles.response import GameRoleItemResponse, GameRoleSetResponse
from ..models.response import ErrorResponse, ResponseMessage, StatusResponse


class GameRoleRepository:
    def __init__(self, broker: RabbitBroker):
        self.broker = broker

    async def get_global_role_templates(
        self,
    ) -> ResponseMessage[list[GameRoleSetResponse] | ErrorResponse]:
        response: RabbitMessage = await rpc_request(self.broker, 
            None, queue="role_set.get_global"
        )
        return ResponseMessage[
            list[GameRoleSetResponse] | ErrorResponse
        ].model_validate_json(response.body)

    async def get_role_set(
        self, access: AccessData
    ) -> ResponseMessage[GameRoleSetResponse | ErrorResponse]:
        access_data = AccessDataRequest(
            member_id=access.member_id,
            server_id=access.server_id,
            permission_mask=access.permission_mask,
            restriction_mask=access.restriction_mask,
        )
        request = GetServerGameRoleSetsRequest(access_data=access_data)
        response: RabbitMessage = await rpc_request(self.broker, 
            request, queue="role_set.get_by_server"
        )
        return ResponseMessage[GameRoleSetResponse | ErrorResponse].model_validate_json(
            response.body
        )

    async def update_role_set(
        self,
        access: AccessData,
        role_set_id: UUID,
        name: str | None = None,
    ) -> ResponseMessage[GameRoleSetResponse | ErrorResponse]:
        access_data = AccessDataRequest(
            member_id=access.member_id,
            server_id=access.server_id,
            permission_mask=access.permission_mask,
            restriction_mask=access.restriction_mask,
        )
        request = GameRoleSetUpdateRequest(
            access_data=access_data, role_set_id=role_set_id, name=name
        )
        response: RabbitMessage = await rpc_request(self.broker, 
            request, queue="role_set.update"
        )
        return ResponseMessage[GameRoleSetResponse | ErrorResponse].model_validate_json(
            response.body
        )

    async def create_role(
        self,
        access: AccessData,
        role_set_id: UUID,
        name: str,
        min_in_team: int,
        max_in_team: int,
        hidden: bool = False,
        icon_id: UUID | None = None,
    ) -> ResponseMessage[GameRoleItemResponse | ErrorResponse]:
        access_data = AccessDataRequest(
            member_id=access.member_id,
            server_id=access.server_id,
            permission_mask=access.permission_mask,
            restriction_mask=access.restriction_mask,
        )
        request = GameRoleItemCreateRequest(
            access_data=access_data,
            role_set_id=role_set_id,
            name=name,
            min_in_team=min_in_team,
            max_in_team=max_in_team,
            hidden=hidden,
            icon_id=icon_id,
        )
        response: RabbitMessage = await rpc_request(self.broker, 
            request, queue="role_set.role.create"
        )
        return ResponseMessage[
            GameRoleItemResponse | ErrorResponse
        ].model_validate_json(response.body)

    async def update_role(
        self,
        access: AccessData,
        role_id: UUID,
        name: str | None = None,
        min_in_team: int | None = None,
        max_in_team: int | None = None,
        hidden: bool | None = None,
        icon_id: UUID | None = None,
    ) -> ResponseMessage[GameRoleItemResponse | ErrorResponse]:
        access_data = AccessDataRequest(
            member_id=access.member_id,
            server_id=access.server_id,
            permission_mask=access.permission_mask,
            restriction_mask=access.restriction_mask,
        )
        request = GameRoleItemUpdateRequest(
            access_data=access_data,
            role_id=role_id,
            name=name,
            min_in_team=min_in_team,
            max_in_team=max_in_team,
            hidden=hidden,
            icon_id=icon_id,
        )
        response: RabbitMessage = await rpc_request(self.broker, 
            request, queue="role_set.role.update"
        )
        return ResponseMessage[
            GameRoleItemResponse | ErrorResponse
        ].model_validate_json(response.body)

    async def delete_role_icon(
        self, access: AccessData, role_id: UUID
    ) -> ResponseMessage[StatusResponse | ErrorResponse]:
        request = GameRoleItemDeleteRequest(
            access_data=AccessDataRequest(
                member_id=access.member_id,
                server_id=access.server_id,
                permission_mask=access.permission_mask,
                restriction_mask=access.restriction_mask,
            ),
            role_id=role_id,
        )
        response: RabbitMessage = await rpc_request(self.broker, 
            request, queue="role_set.role.icon.delete"
        )
        return ResponseMessage[StatusResponse | ErrorResponse].model_validate_json(
            response.body
        )

    async def delete_role(
        self, access: AccessData, role_id: UUID
    ) -> ResponseMessage[StatusResponse | ErrorResponse]:
        request = GameRoleItemDeleteRequest(
            access_data=AccessDataRequest(
                member_id=access.member_id,
                server_id=access.server_id,
                permission_mask=access.permission_mask,
                restriction_mask=access.restriction_mask,
            ),
            role_id=role_id,
        )
        response: RabbitMessage = await rpc_request(self.broker, 
            request, queue="role_set.role.delete"
        )
        return ResponseMessage[StatusResponse | ErrorResponse].model_validate_json(
            response.body
        )
