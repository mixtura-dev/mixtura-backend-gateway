from dataclasses import dataclass, field
from uuid import UUID
from ..models.server.core.response import ServerDetailResponse, ServerListResponse
from ..models.server.game_roles.response import (
    GameRoleItemResponse,
    GameRoleSetResponse,
)
from ..models.server.rating.response import RatingItemResponse, RatingSetResponse
from ..models.server.games.response import GameResponse

import src.infra.communication.server.schemas.core.response as CommunicationCoreResponses
import src.infra.communication.server.schemas.games.response as CommunicationGameResponses
import src.infra.communication.server.schemas.rating.response as CommunicationRatingResponses
import src.infra.communication.server.schemas.game_roles.response as CommunicationGameRoleResponses
import src.infra.communication.server.schemas.member.response as CommunicationMemberResponses


@dataclass
class MappingContext:
    file_urls: dict[str, str] = field(default_factory=dict)


class RatingItemMapper:
    def extract_file_ids(
        self, items: list[CommunicationRatingResponses.RatingItemResponse]
    ) -> set[str]:
        ids = set()
        for item in items:
            if item.icon_id:
                ids.add("rating/icon/" + str(item.icon_id))
        return ids

    def map(
        self,
        items: list[CommunicationRatingResponses.RatingItemResponse],
        context: MappingContext,
    ) -> list[RatingItemResponse]:
        result: list[RatingItemResponse] = []
        for item in items:
            result.append(
                RatingItemResponse(
                    id=item.id,
                    icon_url=context.file_urls.get("rating/icon/" + str(item.icon_id)),
                    threshold=item.threshold,
                )
            )
        return result


class RatingSetMapper:
    def __init__(self) -> None:
        self.rating_item_mapper = RatingItemMapper()

    def extract_file_ids(
        self, items: list[CommunicationRatingResponses.RatingSetResponse]
    ) -> set[str]:
        return self.rating_item_mapper.extract_file_ids(
            [r for item in items for r in item.ratings]
        )

    def map(
        self,
        items: list[CommunicationRatingResponses.RatingSetResponse],
        context: MappingContext,
    ) -> list[RatingSetResponse]:
        result: list[RatingSetResponse] = []
        for item in items:
            ratings = self.rating_item_mapper.map(item.ratings, context)
            result.append(
                RatingSetResponse(
                    id=item.id,
                    name=item.name,
                    min_rating=item.min_rating,
                    max_rating=item.max_rating,
                    is_global=item.is_global,
                    ratings=ratings,
                )
            )
        return result


class GameRoleSetMapper:
    def __init__(self) -> None:
        self.game_role_item_mapper = GameRoleItemMapper()

    def extract_file_ids(
        self, items: list[CommunicationGameRoleResponses.GameRoleSetResponse]
    ) -> set[str]:
        return self.game_role_item_mapper.extract_file_ids(
            [r for item in items for r in item.game_roles]
        )

    def map(
        self,
        items: list[CommunicationGameRoleResponses.GameRoleSetResponse],
        context: MappingContext,
    ) -> list[GameRoleSetResponse]:
        result: list[GameRoleSetResponse] = []
        for item in items:
            game_roles = self.game_role_item_mapper.map(item.game_roles, context)
            result.append(
                GameRoleSetResponse(
                    id=item.id,
                    name=item.name,
                    game_roles=game_roles,
                )
            )
        return result


class GameRoleItemMapper:
    def extract_file_ids(
        self, items: list[CommunicationGameRoleResponses.GameRoleItemResponse]
    ) -> set[str]:
        ids = set()
        for item in items:
            if item.icon_id:
                ids.add("game_role/icon/" + str(item.icon_id))
        return ids

    def map(
        self,
        items: list[CommunicationGameRoleResponses.GameRoleItemResponse],
        context: MappingContext,
    ) -> list[GameRoleItemResponse]:
        result: list[GameRoleItemResponse] = []
        for item in items:
            result.append(
                GameRoleItemResponse(
                    id=item.id,
                    icon_url=context.file_urls.get("game_role/icon/" + str(item.icon_id)),
                    name=item.name,
                    min_in_team=item.min_in_team,
                    max_in_team=item.max_in_team,
                    hidden=item.hidden,
                )
            )
        return result


class GameMapper:
    def extract_file_ids(
        self, games: list[CommunicationGameResponses.GameResponse]
    ) -> set[str]:
        ids = set()
        for g in games:
            if g.icon_id:
                ids.add("game/icon/" + str(g.icon_id))
            if g.banner_id:
                ids.add("game/banner/" + str(g.banner_id))
        return ids

    def map(
        self,
        games: list[CommunicationGameResponses.GameResponse],
        context: MappingContext,
    ) -> list[GameResponse]:
        result: list[GameResponse] = []
        for g in games:
            result.append(
                GameResponse(
                    id=g.id,
                    name=g.name,
                    icon_url=context.file_urls.get("game/icon/" + str(g.icon_id)),
                    banner_url=context.file_urls.get("game/banner/" + str(g.banner_id)),
                )
            )
        return result

class ServerListMapper:
    def extract_file_ids(
        self, servers: list[CommunicationCoreResponses.ServerListResponse]
    ) -> set[str]:
        ids = set()
        for server in servers:
            if server.icon_id:
                ids.add("server/icon/" + str(server.icon_id))
            if server.banner_id:
                ids.add("server/banner/" + str(server.banner_id))
        return ids

    def map(
        self,
        servers: list[CommunicationCoreResponses.ServerListResponse],
        context: MappingContext,
    ) -> list[ServerListResponse]:
        result = []
        for server in servers:
            result.append(
                ServerListResponse(
                    id=server.id,
                    name=server.name,
                    description=server.description,
                    public=server.public,
                    owner_id=server.owner_id,
                    icon_url=context.file_urls.get("server/icon/" + str(server.icon_id))
                    if server.icon_id
                    else None,
                    banner_url=context.file_urls.get(
                        "server/banner/" + str(server.banner_id)
                    )
                    if server.banner_id
                    else None,
                    created_at=server.created_at,
                )
            )
        return result

class ServerDetailMapper:
    def __init__(self) -> None:
        self.rating_set_mapper = RatingSetMapper()
        self.game_role_set_mapper = GameRoleSetMapper()
        self.game_mapper = GameMapper()

    def extract_file_ids(
        self, servers: list[CommunicationCoreResponses.ServerDetailResponse]
    ) -> set[str]:
        ids = set()
        for server in servers:
            if server.icon_id:
                ids.add("server/icon/" + str(server.icon_id))
            if server.banner_id:
                ids.add("server/banner/" + str(server.banner_id))
            if server.rating_set:
                ids.update(self.rating_set_mapper.extract_file_ids([server.rating_set]))
            if server.role_set:
                ids.update(
                    self.game_role_set_mapper.extract_file_ids([server.role_set])
                )
        return ids

    def map(
        self,
        servers: list[CommunicationCoreResponses.ServerDetailResponse],
        context: MappingContext,
    ) -> list[ServerDetailResponse]:
        result = []
        for server in servers:
            result.append(
                ServerDetailResponse(
                    id=server.id,
                    name=server.name,
                    description=server.description,
                    public=server.public,
                    owner_id=server.owner_id,
                    icon_url=context.file_urls.get("server/icon/" + str(server.icon_id))
                    if server.icon_id
                    else None,
                    banner_url=context.file_urls.get(
                        "server/banner/" + str(server.banner_id)
                    )
                    if server.banner_id
                    else None,
                    created_at=server.created_at,
                    rating_set=(
                        next(
                            (rs for rs in self.rating_set_mapper.map([server.rating_set], context) if rs.id == server.rating_set.id),
                            None,
                        )
                        if server.rating_set
                        else None
                    ),
                    role_set=(
                        next(
                            (rs for rs in self.game_role_set_mapper.map([server.role_set], context) if rs.id == server.role_set.id),
                            None,
                        )
                        if server.role_set
                        else None
                    ),
                )
            )
        return result


class RemapperService:
    async def map_server_detail_response(
        self, servers: list[CommunicationCoreResponses.ServerDetailResponse]
    ) -> list[ServerDetailResponse]:
        mapper = ServerDetailMapper()
        file_ids = mapper.extract_file_ids(servers)
        # TODO : fetch file URLs from file service
        file_urls = {}  # TODO : substitute with real URLs
        context = MappingContext(file_urls=file_urls)
        mapped_servers = mapper.map(servers, context)
        return mapped_servers

    async def map_server_list_response(
        self, servers: list[CommunicationCoreResponses.ServerListResponse]
    ) -> list[ServerListResponse]:
        mapper = ServerListMapper()
        file_ids = mapper.extract_file_ids(servers)
        # TODO : fetch file URLs from file service
        file_urls = {}  # TODO : substitute with real URLs
        context = MappingContext(file_urls=file_urls)
        mapped_servers = mapper.map(servers, context)
        return mapped_servers

    async def map_games_response(
        self, games: list[CommunicationGameResponses.GameResponse]
    ) -> list[GameResponse]:
        mapper = GameMapper()
        file_ids = mapper.extract_file_ids(games)
        # TODO : fetch file URLs from file service
        file_urls = {}  # TODO : substitute with real URLs
        context = MappingContext(file_urls=file_urls)
        mapped_games = mapper.map(games, context)
        return mapped_games
    
    async def map_rating_sets_response(
        self, rating_sets: list[CommunicationRatingResponses.RatingSetResponse]
    ) -> list[RatingSetResponse]:
        mapper = RatingSetMapper()
        file_ids = mapper.extract_file_ids(rating_sets)
        # TODO : fetch file URLs from file service
        file_urls = {}  # TODO : substitute with real URLs
        context = MappingContext(file_urls=file_urls)
        mapped_rating_sets = mapper.map(rating_sets, context)
        return mapped_rating_sets
    
    async def map_game_role_sets_response(
        self, game_role_sets: list[CommunicationGameRoleResponses.GameRoleSetResponse]
    ) -> list[GameRoleSetResponse]:
        mapper = GameRoleSetMapper()
        file_ids = mapper.extract_file_ids(game_role_sets)
        # TODO : fetch file URLs from file service
        file_urls = {}  # TODO : substitute with real URLs
        context = MappingContext(file_urls=file_urls)
        mapped_game_role_sets = mapper.map(game_role_sets, context)
        return mapped_game_role_sets
    
    async def map_game_roles_response(
        self, game_roles: list[CommunicationGameRoleResponses.GameRoleItemResponse]
    ) -> list[GameRoleItemResponse]:
        mapper = GameRoleItemMapper()
        file_ids = mapper.extract_file_ids(game_roles)
        # TODO : fetch file URLs from file service
        file_urls = {}  # TODO : substitute with real URLs
        context = MappingContext(file_urls=file_urls)
        mapped_game_roles = mapper.map(game_roles, context)
        return mapped_game_roles
    
    async def map_rating_items_response(
        self, rating_items: list[CommunicationRatingResponses.RatingItemResponse]
    ) -> list[RatingItemResponse]:
        mapper = RatingItemMapper()
        file_ids = mapper.extract_file_ids(rating_items)
        # TODO : fetch file URLs from file service
        file_urls = {}  # TODO : substitute with real URLs
        context = MappingContext(file_urls=file_urls)
        mapped_rating_items = mapper.map(rating_items, context)
        return mapped_rating_items