from uuid import UUID
from fastapi_controllers import Controller, get, put

from ....dependency import (
    AuthorizedUserID,
    MemberServiceDependency,
    RemapperServiceDependency,
    ServerGamesServiceDependency,
)
from src.domain.models.server.games.request import GameSetRequest
from src.domain.models.server.games.response import GameResponse


class ServerGameController(Controller):
    prefix = "/{server_id}/games"
    tags = ["Server game"]

    def __init__(
        self, user_id: AuthorizedUserID, remapper_service: RemapperServiceDependency
    ) -> None:
        self.user_id = user_id
        self.remapper_service = remapper_service

    @get("/", response_model=list[GameResponse])
    async def list_server_games(
        self,
        server_id: UUID,
        game_service: ServerGamesServiceDependency,
        member_service: MemberServiceDependency,
    ):
        access = await member_service.get_member_by_user(server_id, self.user_id)
        server_games = await game_service.list_server_games(access)
        return await self.remapper_service.map_games_response(server_games)

    @put("/", response_model=list[GameResponse])
    async def set_server_games(
        self,
        server_id: UUID,
        body: GameSetRequest,
        game_service: ServerGamesServiceDependency,
        member_service: MemberServiceDependency,
    ):
        access = await member_service.get_member_by_user(server_id, self.user_id)
        server_games = await game_service.set_game(access, body.ids)
        return await self.remapper_service.map_games_response(server_games)
