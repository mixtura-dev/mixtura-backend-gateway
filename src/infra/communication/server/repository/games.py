from uuid import UUID
from faststream.rabbit import RabbitBroker, RabbitMessage

from ..schemas.games.request import (
    GameAddRequest,
    GameRemoveRequest,
    GameSetRequest,
    GetServerGameListRequest,
)
from ..schemas.request import AccessDataRequest
from ..schemas.games.response import GameResponse
from ..schemas.response import ErrorResponse, ResponseMessage


class GameRepository:
    def __init__(self, broker: RabbitBroker):
        self.broker = broker

    async def get_global_games(
        self,
    ) -> ResponseMessage[list[GameResponse] | ErrorResponse]:
        response: RabbitMessage = await self.broker.request(
            None, queue="server.global.games"
        )
        return ResponseMessage[list[GameResponse] | ErrorResponse].model_validate_json(
            response.body
        )

    async def add_game(
        self, access_data: AccessDataRequest, game_ids: list[UUID]
    ) -> ResponseMessage[list[GameResponse] | ErrorResponse]:
        request = GameAddRequest(access_data=access_data, game_ids=game_ids)
        response: RabbitMessage = await self.broker.request(
            request, queue="game.server.add"
        )
        return ResponseMessage[list[GameResponse] | ErrorResponse].model_validate_json(
            response.body
        )

    async def remove_game(
        self, access_data: AccessDataRequest, game_id: UUID
    ) -> ResponseMessage[list[GameResponse] | ErrorResponse]:
        request = GameRemoveRequest(access_data=access_data, game_id=game_id)
        response: RabbitMessage = await self.broker.request(
            request, queue="game.server.remove"
        )
        return ResponseMessage[list[GameResponse] | ErrorResponse].model_validate_json(
            response.body
        )

    async def set_game(
        self, access_data: AccessDataRequest, game_ids: list[UUID]
    ) -> ResponseMessage[list[GameResponse] | ErrorResponse]:
        request = GameSetRequest(access_data=access_data, game_ids=game_ids)
        response: RabbitMessage = await self.broker.request(
            request, queue="game.server.set"
        )
        return ResponseMessage[list[GameResponse] | ErrorResponse].model_validate_json(
            response.body
        )

    async def list_server_games(
        self, access_data: AccessDataRequest
    ) -> ResponseMessage[list[GameResponse] | ErrorResponse]:
        request = GetServerGameListRequest(access_data=access_data)
        response: RabbitMessage = await self.broker.request(
            request, queue="game.server.list"
        )
        return ResponseMessage[list[GameResponse] | ErrorResponse].model_validate_json(
            response.body
        )
