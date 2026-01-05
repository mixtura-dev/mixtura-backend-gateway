from uuid import UUID
from faststream.rabbit import RabbitBroker, RabbitMessage
from ..schemas.game_roles.request import (
    GameRoleItemCreateRequest,
    GameRoleItemDeleteRequest,
    GameRoleItemUpdateRequest,
    GameRoleSetUpdateRequest,
    GetServerGameRoleSetsRequest,
)
from ..schemas.request import AccessDataRequest
from ..schemas.game_roles.response import GameRoleItemResponse, GameRoleSetResponse
from ..schemas.response import ErrorResponse, ResponseMessage, StatusResponse


class GameRoleRepository:
    def __init__(self, broker: RabbitBroker):
        self.broker = broker

    async def get_global_role_templates(
        self,
    ) -> ResponseMessage[list[GameRoleSetResponse] | ErrorResponse]:
        response: RabbitMessage = await self.broker.request(
            None, queue="role_set.get_global"
        )
        return ResponseMessage[
            list[GameRoleSetResponse] | ErrorResponse
        ].model_validate_json(response.body)

    async def get_role_set(
        self, access_data: AccessDataRequest
    ) -> ResponseMessage[GameRoleSetResponse | ErrorResponse]:
        request = GetServerGameRoleSetsRequest(access_data=access_data)
        response: RabbitMessage = await self.broker.request(
            request, queue="role_set.get_by_server"
        )
        return ResponseMessage[GameRoleSetResponse | ErrorResponse].model_validate_json(
            response.body
        )

    async def update_role_set(
        self,
        access_data: AccessDataRequest,
        role_set_id: UUID,
        name: str | None = None,
    ) -> ResponseMessage[GameRoleSetResponse | ErrorResponse]:
        request = GameRoleSetUpdateRequest(
            access_data=access_data, role_set_id=role_set_id, name=name
        )
        response: RabbitMessage = await self.broker.request(
            request, queue="role_set.update"
        )
        return ResponseMessage[GameRoleSetResponse | ErrorResponse].model_validate_json(
            response.body
        )

    async def create_role(
        self,
        access_data: AccessDataRequest,
        role_set_id: UUID,
        role_id: UUID,
        name: str,
        min_in_team: int,
        max_in_team: int,
        hidden: bool = False,
        icon_id: UUID | None = None,
    ) -> ResponseMessage[GameRoleItemResponse | ErrorResponse]:
        request = GameRoleItemCreateRequest(
            access_data=access_data,
            role_set_id=role_set_id,
            role_id=role_id,
            name=name,
            min_in_team=min_in_team,
            max_in_team=max_in_team,
            hidden=hidden,
            icon_id=icon_id,
        )
        response: RabbitMessage = await self.broker.request(
            request, queue="role_set.role.create"
        )
        return ResponseMessage[
            GameRoleItemResponse | ErrorResponse
        ].model_validate_json(response.body)

    async def update_role(
        self,
        access_data: AccessDataRequest,
        role_id: UUID,
        name: str | None = None,
        min_in_team: int | None = None,
        max_in_team: int | None = None,
        hidden: bool | None = None,
        icon_id: UUID | None = None,
    ) -> ResponseMessage[GameRoleItemResponse | ErrorResponse]:
        request = GameRoleItemUpdateRequest(
            access_data=access_data,
            role_id=role_id,
            name=name,
            min_in_team=min_in_team,
            max_in_team=max_in_team,
            hidden=hidden,
            icon_id=icon_id,
        )
        response: RabbitMessage = await self.broker.request(
            request, queue="role_set.role.update"
        )
        return ResponseMessage[
            GameRoleItemResponse | ErrorResponse
        ].model_validate_json(response.body)

    async def delete_role_icon(
        self, access_data: AccessDataRequest, role_id: UUID
    ) -> ResponseMessage[StatusResponse | ErrorResponse]:
        request = GameRoleItemDeleteRequest(access_data=access_data, role_id=role_id)
        response: RabbitMessage = await self.broker.request(
            request, queue="role_set.role.icon.delete"
        )
        return ResponseMessage[StatusResponse | ErrorResponse].model_validate_json(
            response.body
        )

    async def delete_role(
        self, access_data: AccessDataRequest, role_id: UUID
    ) -> ResponseMessage[StatusResponse | ErrorResponse]:
        request = GameRoleItemDeleteRequest(access_data=access_data, role_id=role_id)
        response: RabbitMessage = await self.broker.request(
            request, queue="role_set.role.delete"
        )
        return ResponseMessage[StatusResponse | ErrorResponse].model_validate_json(
            response.body
        )
