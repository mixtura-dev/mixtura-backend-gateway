from uuid import UUID

from src.infra.communication.rabbit import RabbitRpcClient
from src.infra.communication.rpc import rpc_request

from ..models.games.request import (
    GameAddRequest,
    GameRemoveRequest,
    GameSetRequest,
    GetServerGameListRequest,
)
from ..models.request import AccessDataRequest
from src.domain.models.access import AccessData
from ..models.games.response import GameResponse
from ..models.response import ErrorResponse, ResponseMessage


class ServerGameRepository:
    def __init__(self, rpc_client: RabbitRpcClient):
        self.rpc_client = rpc_client

    async def get_global_games(
        self,
    ) -> ResponseMessage[list[GameResponse] | ErrorResponse]:
        response = await rpc_request(self.rpc_client,
            None, queue="server.global.games"
        )
        return ResponseMessage[list[GameResponse] | ErrorResponse].model_validate_json(
            response.body
        )

    async def add_game(
        self, access: AccessData, game_ids: list[UUID]
    ) -> ResponseMessage[list[GameResponse] | ErrorResponse]:
        access_data = AccessDataRequest(
            member_id=access.member_id,
            server_id=access.server_id,
            permission_mask=access.permission_mask,
            restriction_mask=access.restriction_mask,
        )
        request = GameAddRequest(access_data=access_data, game_ids=game_ids)
        response = await rpc_request(self.rpc_client,
            request, queue="game.server.add"
        )
        return ResponseMessage[list[GameResponse] | ErrorResponse].model_validate_json(
            response.body
        )

    async def remove_game(
        self, access: AccessData, game_id: UUID
    ) -> ResponseMessage[list[GameResponse] | ErrorResponse]:
        access_data = AccessDataRequest(
            member_id=access.member_id,
            server_id=access.server_id,
            permission_mask=access.permission_mask,
            restriction_mask=access.restriction_mask,
        )
        request = GameRemoveRequest(access_data=access_data, game_id=game_id)
        response = await rpc_request(self.rpc_client,
            request, queue="game.server.remove"
        )
        return ResponseMessage[list[GameResponse] | ErrorResponse].model_validate_json(
            response.body
        )

    async def set_game(
        self, access: AccessData, game_ids: list[UUID]
    ) -> ResponseMessage[list[GameResponse] | ErrorResponse]:
        access_data = AccessDataRequest(
            member_id=access.member_id,
            server_id=access.server_id,
            permission_mask=access.permission_mask,
            restriction_mask=access.restriction_mask,
        )
        request = GameSetRequest(access_data=access_data, game_ids=game_ids)
        response = await rpc_request(self.rpc_client,
            request, queue="game.server.set"
        )
        return ResponseMessage[list[GameResponse] | ErrorResponse].model_validate_json(
            response.body
        )

    async def list_server_games(
        self, access: AccessData
    ) -> ResponseMessage[list[GameResponse] | ErrorResponse]:
        access_data = AccessDataRequest(
            member_id=access.member_id,
            server_id=access.server_id,
            permission_mask=access.permission_mask,
            restriction_mask=access.restriction_mask,
        )
        request = GetServerGameListRequest(access_data=access_data)
        response = await rpc_request(self.rpc_client,
            request, queue="game.server.list"
        )
        return ResponseMessage[list[GameResponse] | ErrorResponse].model_validate_json(
            response.body
        )
