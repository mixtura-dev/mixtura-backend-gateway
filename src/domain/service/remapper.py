from dataclasses import dataclass, field
from uuid import UUID

from ..models.server.member.response import ReducedMemberResponse

from ..models.server.custom.response import CustomRatingResponse, CustomResponse
from ..models.server.core.response import ServerDetailResponse, ServerListResponse
from ..models.server.game_roles.response import (
    GameRoleItemResponse,
    GameRoleSetResponse,
)
from ..models.server.rating.response import RatingItemResponse, RatingSetResponse
from ..models.server.games.response import GameResponse
from ..models.mixer.response import (
    ApplicationDetailResponse,
    ApplicationFilledFieldResponse,
    ApplicationIntegrationItemResponse,
    ApplicationIntegrationResponse,
    ApplicationListItemResponse,
    ApplicationListItemUserResponse,
    ApplicationRoleItemResponse,
    ApplicationRolePriorityResponse,
    DraftDetailResponse,
    DraftedPlayerItemResponse,
    DraftItemResponse,
    EventPlayerResponse,
    OrganizerResponse,
    PlayerUpdateResultResponse,
    RecordedMatchResultResponse,
    SingleMatchSlotViewResponse,
    SingleMatchViewResponse,
)

import src.infra.communication.server.models.core.response as CommunicationCoreResponses
import src.infra.communication.server.models.games.response as CommunicationGameResponses
import src.infra.communication.server.models.rating.response as CommunicationRatingResponses
import src.infra.communication.server.models.game_roles.response as CommunicationGameRoleResponses
import src.infra.communication.server.models.custom.response as CommunicationCustomResponses
import src.infra.communication.mixer.models.response as CommunicationMixerResponses


@dataclass
class MappingContext:
    file_urls: dict[str, str] = field(default_factory=dict)
    member_info: dict[UUID, ReducedMemberResponse] = field(default_factory=dict)
    user_info: dict[UUID, object] = field(default_factory=dict)
    integration_names: dict[UUID, str] = field(default_factory=dict)
    custom_info: dict[UUID, CustomResponse] = field(default_factory=dict)


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
                    icon_url=context.file_urls.get(
                        "game_role/icon/" + str(item.icon_id)
                    ),
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
                            (
                                rs
                                for rs in self.rating_set_mapper.map(
                                    [server.rating_set], context
                                )
                                if rs.id == server.rating_set.id
                            ),
                            None,
                        )
                        if server.rating_set
                        else None
                    ),
                    role_set=(
                        next(
                            (
                                rs
                                for rs in self.game_role_set_mapper.map(
                                    [server.role_set], context
                                )
                                if rs.id == server.role_set.id
                            ),
                            None,
                        )
                        if server.role_set
                        else None
                    ),
                )
            )
        return result


class CustomRatingMapper:
    def __init__(self) -> None:
        self.game_role_item_mapper = GameRoleItemMapper()

    def extract_file_ids(
        self, items: list[CommunicationCustomResponses.CustomRatingResponse]
    ) -> set[str]:
        return self.game_role_item_mapper.extract_file_ids(
            [item.game_role for item in items]
        )

    def map(
        self,
        items: list[CommunicationCustomResponses.CustomRatingResponse],
        context: MappingContext,
    ) -> list[CustomRatingResponse]:
        result: list[CustomRatingResponse] = []
        for item in items:
            game_role = self.game_role_item_mapper.map([item.game_role], context)[0]
            result.append(
                CustomRatingResponse(
                    game_role=game_role,
                    rating=item.rating,
                )
            )
        return result


class CustomMapper:
    def __init__(self) -> None:
        self.custom_rating_mapper = CustomRatingMapper()

    def extract_file_ids(
        self, items: list[CommunicationCustomResponses.CustomResponse]
    ) -> set[str]:
        return self.custom_rating_mapper.extract_file_ids(
            [r for item in items for r in item.custom_ratings]
        )

    def map(
        self,
        items: list[CommunicationCustomResponses.CustomResponse],
        context: MappingContext,
    ) -> list[CustomResponse]:
        result: list[CustomResponse] = []
        for item in items:
            custom_ratings = self.custom_rating_mapper.map(item.custom_ratings, context)
            result.append(
                CustomResponse(
                    id=item.id,
                    member=ReducedMemberResponse.model_validate(
                        item.member
                    ),  # Assuming direct mapping; adjust if needed
                    creator=ReducedMemberResponse.model_validate(
                        item.creator
                    ),  # Assuming direct mapping; adjust if needed
                    custom_ratings=custom_ratings,
                )
            )
        return result


class ApplicationMapper:
    def extract_member_ids(
        self, items: list[CommunicationMixerResponses.ApplicationListItem],
    ) -> set[UUID]:
        return {item.member_id for item in items}

    def map(
        self,
        items: list[CommunicationMixerResponses.ApplicationListItem],
        context: MappingContext,
    ) -> list[ApplicationListItemResponse]:
        result: list[ApplicationListItemResponse] = []
        for item in items:
            mid = item.member_id
            member = context.member_info.get(mid)
            uid = member.user_id if member and member.user_id else None
            user_obj = context.user_info.get(uid) if uid else None
            user_info: ApplicationListItemUserResponse | None = None
            if user_obj:
                user_info = ApplicationListItemUserResponse(
                    id=getattr(user_obj, "id", uid),
                    username=getattr(user_obj, "username", None),
                )

            roles: list[ApplicationRoleItemResponse] = []
            for role_data in item.roles:
                roles.append(ApplicationRoleItemResponse(
                    role_id=role_data.role_id,
                    game_role_id=role_data.game_role_id,
                    priority=role_data.priority,
                ))

            integrations: list[ApplicationIntegrationItemResponse] = []
            for int_data in item.integrations:
                integration_id = int_data.integration_id
                integrations.append(ApplicationIntegrationItemResponse(
                    integration_id=integration_id,
                    provider_id=int_data.provider_id,
                    provider_name=int_data.provider_name,
                    account_name=context.integration_names.get(integration_id),
                ))

            result.append(ApplicationListItemResponse(
                id=item.id,
                member_id=mid,
                status=item.status.value,
                is_approved=item.is_approved,
                created_at=item.created_at,
                user=user_info,
                roles=roles,
                integrations=integrations,
            ))
        return result


class PlayerMapper:
    def extract_member_ids(
        self, items: list[CommunicationMixerResponses.PlayerItem],
    ) -> set[UUID]:
        return {item.member_id for item in items}

    def extract_custom_ids(
        self, items: list[CommunicationMixerResponses.PlayerUpdateResult],
    ) -> set[UUID]:
        return {item.custom_id for item in items if item.custom_id}

    def map_players(
        self,
        items: list[CommunicationMixerResponses.PlayerItem],
        context: MappingContext,
    ) -> list[EventPlayerResponse]:
        result: list[EventPlayerResponse] = []
        for item in items:
            mid = item.member_id
            member = context.member_info.get(mid)
            result.append(EventPlayerResponse(
                id=item.id,
                member=member if member else ReducedMemberResponse(id=mid, nickname=None, user_id=None),
                status=item.status,
                is_draft_pinned=item.is_draft_pinned,
                application_id=item.application_id,
            ))
        return result

    def map_update_result(
        self,
        item: CommunicationMixerResponses.PlayerUpdateResult,
        context: MappingContext,
    ) -> PlayerUpdateResultResponse:
        mid = item.member_id
        member = context.member_info.get(mid)
        custom = context.custom_info.get(item.custom_id) if item.custom_id else None
        return PlayerUpdateResultResponse(
            id=item.id,
            member=member if member else ReducedMemberResponse(id=mid, nickname=None, user_id=None),
            status=item.status,
            custom=custom,
        )


class DraftMapper:
    def map_detail(
        self,
        item: CommunicationMixerResponses.DraftDetail,
    ) -> DraftDetailResponse:
        drafted_players = [
            DraftedPlayerItemResponse(
                id=p.id,
                draft_id=p.draft_id,
                event_player_id=p.event_player_id,
                is_captain=p.is_captain,
            )
            for p in item.drafted_players
        ]
        return DraftDetailResponse(
            id=item.id,
            event_id=item.event_id,
            status=item.status.value if hasattr(item.status, 'value') else item.status,
            drafted_players=drafted_players,
        )

    def map_items(
        self,
        items: list[CommunicationMixerResponses.DraftItem],
    ) -> list[DraftItemResponse]:
        return [
            DraftItemResponse(
                id=item.id,
                event_id=item.event_id,
                status=item.status.value if hasattr(item.status, 'value') else item.status,
            )
            for item in items
        ]


class EventDetailOrganizerMapper:
    def extract_member_ids(
        self, organizers: list[CommunicationMixerResponses.OrganizerData],
    ) -> set[UUID]:
        return {org.member_id for org in organizers}

    def map(
        self,
        organizers: list[CommunicationMixerResponses.OrganizerData],
        context: MappingContext,
    ) -> list[OrganizerResponse]:
        result: list[OrganizerResponse] = []
        for org in organizers:
            member = context.member_info.get(org.member_id)
            result.append(OrganizerResponse(
                id=org.id,
                member_id=org.member_id,
            ))
        return result


class ApplicationDetailMapper:
    def extract_member_ids(
        self, item: CommunicationMixerResponses.ApplicationDetail,
    ) -> set[UUID]:
        return {item.member_id}

    def map(
        self,
        item: CommunicationMixerResponses.ApplicationDetail,
        context: MappingContext,
    ) -> ApplicationDetailResponse:
        mid = item.member_id
        member = context.member_info.get(mid)
        uid = member.user_id if member and member.user_id else None
        user_obj = context.user_info.get(uid) if uid else None
        user_info = None
        if user_obj:
            user_info = ApplicationListItemUserResponse(
                id=getattr(user_obj, "id", uid),
                username=getattr(user_obj, "username", None),
            )

        role_priorities = [
            ApplicationRolePriorityResponse(
                role_id=rp.role_id,
                priority=rp.priority,
            )
            for rp in item.role_priorities
        ]

        integrations = [
            ApplicationIntegrationResponse(
                integration_id=inv.integration_id,
                provider_id=inv.provider_id,
                provider_name=inv.provider_name,
            )
            for inv in item.integrations
        ]

        return ApplicationDetailResponse(
            id=item.id,
            event_id=item.event_id,
            member_id=mid,
            status=item.status.value if hasattr(item.status, 'value') else item.status,
            role_priorities=role_priorities,
            filled_fields=[
                ApplicationFilledFieldResponse(
                    custom_field_id=ff.custom_field_id,
                    value=ff.value,
                )
                for ff in item.filled_fields
            ],
            integrations=integrations,
            event_player_id=item.event_player_id,
        )


class MatchMapper:
    def extract_team_ids_from_view(
        self, matches: list[CommunicationMixerResponses.SingleMatchView],
    ) -> set[UUID]:
        ids: set[UUID] = set()
        for match in matches:
            for slot in match.slots:
                ids.add(slot.team_id)
            if match.result_snapshot and isinstance(match.result_snapshot, dict):
                winner_id = match.result_snapshot.get("winner_team_id")
                if winner_id:
                    ids.add(winner_id)
                loser_ids = match.result_snapshot.get("loser_team_ids", [])
                for tid in loser_ids:
                    ids.add(tid)
        return ids

    def extract_team_ids_from_result(
        self, result: CommunicationMixerResponses.RecordedMatchResult,
    ) -> set[UUID]:
        ids: set[UUID] = set()
        if result.winner_team_id:
            ids.add(result.winner_team_id)
        for tid in result.loser_team_ids:
            ids.add(tid)
        for slot in result.match.slots:
            ids.add(slot.team_id)
        return ids

    def map_single_view(
        self,
        match: CommunicationMixerResponses.SingleMatchView,
        context: MappingContext,
    ) -> SingleMatchViewResponse:
        return SingleMatchViewResponse(
            event_id=match.event_id,
            bracket_id=match.bracket_id,
            stage_id=match.stage_id,
            group_id=match.group_id,
            match_id=match.match_id,
            match_index=match.match_index,
            draft_id=match.draft_id,
            completed_at=match.completed_at,
            result_snapshot=match.result_snapshot,
            slots=[
                SingleMatchSlotViewResponse(
                    slot_id=s.slot_id,
                    slot_num=s.slot_num,
                    team_id=s.team_id,
                    score_id=s.score_id,
                    score=s.score,
                )
                for s in match.slots
            ],
        )

    def map_result(
        self,
        result: CommunicationMixerResponses.RecordedMatchResult,
        context: MappingContext,
    ) -> RecordedMatchResultResponse:
        return RecordedMatchResultResponse(
            match=self.map_single_view(result.match, context),
            winner_team_id=result.winner_team_id,
            loser_team_ids=result.loser_team_ids,
            is_draw=result.is_draw,
            forfeit_team_ids=result.forfeit_team_ids,
            team_ranks=result.team_ranks,
            rating_payload=result.rating_payload,
            rating_published=result.rating_published,
        )


class RemapperService:
    async def _fetch_file_urls(self, file_ids: set[str]) -> dict[str, str]:
        # TODO : implement actual file URL fetching logic
        return {file_id: f"https://static.demogram.ru/mixtura/{file_id}" for file_id in file_ids}

    async def map_server_detail_response(
        self, servers: list[CommunicationCoreResponses.ServerDetailResponse]
    ) -> list[ServerDetailResponse]:
        mapper = ServerDetailMapper()
        file_ids = mapper.extract_file_ids(servers)
        file_urls = await self._fetch_file_urls(file_ids)
        context = MappingContext(file_urls=file_urls)
        mapped_servers = mapper.map(servers, context)
        return mapped_servers

    async def map_server_list_response(
        self, servers: list[CommunicationCoreResponses.ServerListResponse]
    ) -> list[ServerListResponse]:
        mapper = ServerListMapper()
        file_ids = mapper.extract_file_ids(servers)
        file_urls = await self._fetch_file_urls(file_ids)
        context = MappingContext(file_urls=file_urls)
        mapped_servers = mapper.map(servers, context)
        return mapped_servers

    async def map_games_response(
        self, games: list[CommunicationGameResponses.GameResponse]
    ) -> list[GameResponse]:
        mapper = GameMapper()
        file_ids = mapper.extract_file_ids(games)
        file_urls = await self._fetch_file_urls(file_ids)
        context = MappingContext(file_urls=file_urls)
        mapped_games = mapper.map(games, context)
        return mapped_games

    async def map_rating_sets_response(
        self, rating_sets: list[CommunicationRatingResponses.RatingSetResponse]
    ) -> list[RatingSetResponse]:
        mapper = RatingSetMapper()
        file_ids = mapper.extract_file_ids(rating_sets)
        file_urls = await self._fetch_file_urls(file_ids)
        context = MappingContext(file_urls=file_urls)
        mapped_rating_sets = mapper.map(rating_sets, context)
        return mapped_rating_sets

    async def map_game_role_sets_response(
        self, game_role_sets: list[CommunicationGameRoleResponses.GameRoleSetResponse]
    ) -> list[GameRoleSetResponse]:
        mapper = GameRoleSetMapper()
        file_ids = mapper.extract_file_ids(game_role_sets)
        file_urls = await self._fetch_file_urls(file_ids)
        context = MappingContext(file_urls=file_urls)
        mapped_game_role_sets = mapper.map(game_role_sets, context)
        return mapped_game_role_sets

    async def map_game_roles_response(
        self, game_roles: list[CommunicationGameRoleResponses.GameRoleItemResponse]
    ) -> list[GameRoleItemResponse]:
        mapper = GameRoleItemMapper()
        file_ids = mapper.extract_file_ids(game_roles)
        file_urls = await self._fetch_file_urls(file_ids)
        context = MappingContext(file_urls=file_urls)
        mapped_game_roles = mapper.map(game_roles, context)
        return mapped_game_roles

    async def map_rating_items_response(
        self, rating_items: list[CommunicationRatingResponses.RatingItemResponse]
    ) -> list[RatingItemResponse]:
        mapper = RatingItemMapper()
        file_ids = mapper.extract_file_ids(rating_items)
        file_urls = await self._fetch_file_urls(file_ids)
        context = MappingContext(file_urls=file_urls)
        mapped_rating_items = mapper.map(rating_items, context)
        return mapped_rating_items

    async def map_customs_response(
        self, customs: list[CommunicationCustomResponses.CustomResponse]
    ) -> list[CustomResponse]:
        mapper = CustomMapper()
        file_ids = mapper.extract_file_ids(customs)
        file_urls = await self._fetch_file_urls(file_ids)
        context = MappingContext(file_urls=file_urls)
        mapped_customs = mapper.map(customs, context)
        return mapped_customs

    async def map_applications_response(
        self,
        applications: list[CommunicationMixerResponses.ApplicationListItem],
        member_info: dict[UUID, ReducedMemberResponse],
        user_info: dict[UUID, object],
        integration_names: dict[UUID, str],
    ) -> list[ApplicationListItemResponse]:
        mapper = ApplicationMapper()
        context = MappingContext(member_info=member_info, user_info=user_info, integration_names=integration_names)
        return mapper.map(applications, context)

    async def map_players_response(
        self,
        players: list[CommunicationMixerResponses.PlayerItem],
        member_info: dict[UUID, ReducedMemberResponse],
    ) -> list[EventPlayerResponse]:
        mapper = PlayerMapper()
        context = MappingContext(member_info=member_info)
        return mapper.map_players(players, context)

    async def map_player_update_result_response(
        self,
        result: CommunicationMixerResponses.PlayerUpdateResult,
        member_info: dict[UUID, ReducedMemberResponse],
        custom_info: dict[UUID, CustomResponse],
    ) -> PlayerUpdateResultResponse:
        mapper = PlayerMapper()
        context = MappingContext(member_info=member_info, custom_info=custom_info)
        return mapper.map_update_result(result, context)

    async def map_draft_detail_response(
        self, draft: CommunicationMixerResponses.DraftDetail,
    ) -> DraftDetailResponse:
        mapper = DraftMapper()
        return mapper.map_detail(draft)

    async def map_draft_items_response(
        self, drafts: list[CommunicationMixerResponses.DraftItem],
    ) -> list[DraftItemResponse]:
        mapper = DraftMapper()
        return mapper.map_items(drafts)

    async def map_event_detail_organizers(
        self,
        organizers: list[CommunicationMixerResponses.OrganizerData],
        member_info: dict[UUID, ReducedMemberResponse],
    ) -> list[OrganizerResponse]:
        mapper = EventDetailOrganizerMapper()
        context = MappingContext(member_info=member_info)
        return mapper.map(organizers, context)

    async def map_application_detail_response(
        self,
        application: CommunicationMixerResponses.ApplicationDetail,
        member_info: dict[UUID, ReducedMemberResponse],
        user_info: dict[UUID, object],
    ) -> ApplicationDetailResponse:
        mapper = ApplicationDetailMapper()
        context = MappingContext(member_info=member_info, user_info=user_info)
        return mapper.map(application, context)

    async def map_match_view_response(
        self,
        match: CommunicationMixerResponses.SingleMatchView,
    ) -> SingleMatchViewResponse:
        mapper = MatchMapper()
        context = MappingContext()
        return mapper.map_single_view(match, context)

    async def map_match_result_response(
        self,
        result: CommunicationMixerResponses.RecordedMatchResult,
    ) -> RecordedMatchResultResponse:
        mapper = MatchMapper()
        context = MappingContext()
        return mapper.map_result(result, context)
