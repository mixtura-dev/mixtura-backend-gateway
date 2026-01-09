from uuid import UUID
from ..exceptions import ServiceException
from src.infra.communication.server.repository.games import ServerGameRepository
from src.infra.communication.server.models.response import ErrorResponse
from src.infra.communication.server.models.games.response import GameResponse
from src.domain.models.access import AccessData


class ServerGamesService:
    def __init__(self, games_repository: ServerGameRepository) -> None:
        self.games_repository = games_repository

    async def get_global_games(self) -> list[GameResponse]:
        response = await self.games_repository.get_global_games()
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message

    async def add_game(self, access: AccessData, game_ids: list[UUID]) -> list[GameResponse]:
        response = await self.games_repository.add_game(access, game_ids)
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message

    async def remove_game(self, access: AccessData, game_id: UUID) -> list[GameResponse]:
        response = await self.games_repository.remove_game(access, game_id)
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message

    async def set_game(self, access: AccessData, game_ids: list[UUID]) -> list[GameResponse]:
        response = await self.games_repository.set_game(access, game_ids)
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message

    async def list_server_games(self, access: AccessData) -> list[GameResponse]:
        response = await self.games_repository.list_server_games(access)
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message
