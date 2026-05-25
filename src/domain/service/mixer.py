from uuid import UUID

from src.domain.exceptions import ServiceException
from src.domain.models.access import AccessData
from src.infra.communication.mixer.models.shared import ErrorResponse, PaginationRequest
from src.infra.communication.mixer.models.requests.team_formation import (
    RatingSnapshotInput,
)
from src.infra.communication.mixer.repository import MixerEventRepository
from src.infra.communication.server.repository.custom import MemberCustomRepository
from src.infra.communication.server.repository.game_roles import GameRoleRepository
from src.infra.communication.server.repository.member import MemberRepository
from src.infra.communication.server.models.response import ErrorResponse as ServerErrorResponse
from src.infra.communication.server.models.custom.response import CustomResponse as InfraCustomResponse
from src.infra.communication.server.repository.rating import RatingRepository


class MixerEventService:
    def __init__(
        self,
        event_repository: MixerEventRepository,
        rating_repository: RatingRepository,
        member_repository: MemberRepository,
        game_role_repository: GameRoleRepository,
        custom_repository: MemberCustomRepository,
        auth_service=None,
    ) -> None:
        self.event_repository = event_repository
        self.rating_repository = rating_repository
        self.member_repository = member_repository
        self.game_role_repository = game_role_repository
        self.custom_repository = custom_repository
        self.auth_service = auth_service

    def _unwrap(self, response):
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message

    async def _get_server_rating_set_id(self, access: AccessData) -> UUID:
        response = await self.rating_repository.get_rating_set(access)
        if isinstance(response.message, ServerErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message.id

    async def _ensure_member_exists(self, access: AccessData, member_id: UUID) -> None:
        response = await self.member_repository.get_member(access, member_id)
        if isinstance(response.message, ServerErrorResponse):
            raise ServiceException(response.status, response.message.message)

    async def _ensure_game_roles_exist(
        self, access: AccessData, game_role_ids: set[UUID]
    ) -> None:
        if not game_role_ids:
            return

        response = await self.game_role_repository.get_role_set(access)
        if isinstance(response.message, ServerErrorResponse):
            raise ServiceException(response.status, response.message.message)

        existing_role_ids = {role.id for role in response.message.game_roles}
        missing_role_ids = game_role_ids.difference(existing_role_ids)
        if missing_role_ids:
            raise ServiceException(404, "Game role not found for server")

    async def health(self):
        return self._unwrap(await self.event_repository.health())

    async def create_event(self, access: AccessData, body):
        rating_set_id = await self._get_server_rating_set_id(access)
        return self._unwrap(await self.event_repository.create_event(access, body, rating_set_id))

    async def get_event(self, access: AccessData, event_id: UUID):
        return self._unwrap(await self.event_repository.get_event(access, event_id))

    async def update_event(self, access: AccessData, event_id: UUID, body):
        return self._unwrap(
            await self.event_repository.update_event(access, event_id, body)
        )

    async def activate_event(self, access: AccessData, event_id: UUID):
        return self._unwrap(await self.event_repository.activate_event(access, event_id))

    async def open_registration(self, access: AccessData, event_id: UUID):
        return self._unwrap(
            await self.event_repository.open_registration(access, event_id)
        )

    async def close_registration(self, access: AccessData, event_id: UUID):
        return self._unwrap(
            await self.event_repository.close_registration(access, event_id)
        )

    async def cancel_event(self, access: AccessData, event_id: UUID):
        return self._unwrap(await self.event_repository.cancel_event(access, event_id))

    async def complete_event(self, access: AccessData, event_id: UUID):
        return self._unwrap(await self.event_repository.complete_event(access, event_id))

    async def list_organizers(
        self, access: AccessData, event_id: UUID, page: int, page_size: int
    ):
        return self._unwrap(
            await self.event_repository.list_organizers(
                access, event_id, PaginationRequest(page=page, page_size=page_size)
            )
        )

    async def add_organizer(
        self, access: AccessData, event_id: UUID, member_id: UUID
    ):
        await self._ensure_member_exists(access, member_id)
        return self._unwrap(
            await self.event_repository.add_organizer(access, event_id, member_id)
        )

    async def remove_organizer(
        self, access: AccessData, event_id: UUID, member_id: UUID
    ):
        return self._unwrap(
            await self.event_repository.remove_organizer(access, event_id, member_id)
        )

    async def _resolve_application_integrations(self, body, user_id: UUID):
        if not body.integrations:
            return []
        if self.auth_service is None:
            raise ServiceException(500, "Auth service is not configured")

        user = await self.auth_service.get_user(user_id)
        providers_by_id = {provider.id: provider for provider in user.providers}
        missing = [
            str(integration.integration_id)
            for integration in body.integrations
            if integration.integration_id not in providers_by_id
        ]
        if missing:
            raise ServiceException(404, f"Integration not found: {', '.join(missing)}")

        return [
            {
                "integration_id": integration.integration_id,
                "provider_id": providers_by_id[integration.integration_id].id,
                "provider_name": providers_by_id[integration.integration_id].name,
            }
            for integration in body.integrations
        ]

    async def submit_application(self, access: AccessData, event_id: UUID, body, user_id: UUID):
        integrations = await self._resolve_application_integrations(body, user_id)
        return self._unwrap(
            await self.event_repository.submit_application(
                access, event_id, body, integrations
            )
        )

    async def get_application(self, access: AccessData, application_id: UUID):
        return self._unwrap(
            await self.event_repository.get_application(access, application_id)
        )

    async def list_applications(
        self,
        access: AccessData,
        event_id: UUID,
        status: str | None,
        page: int,
        page_size: int,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ):
        return self._unwrap(
            await self.event_repository.list_applications(
                access,
                event_id,
                status,
                PaginationRequest(page=page, page_size=page_size),
                sort_by,
                sort_order,
            )
        )

    async def review_application(self, access: AccessData, application_id: UUID, body):
        return self._unwrap(
            await self.event_repository.review_application(access, application_id, body)
        )

    async def list_players(
        self,
        access: AccessData,
        event_id: UUID,
        status: str | None,
        page: int,
        page_size: int,
    ):
        return self._unwrap(
            await self.event_repository.list_players(
                access,
                event_id,
                status,
                PaginationRequest(page=page, page_size=page_size),
            )
        )

    async def update_player_status(
        self, access: AccessData, event_id: UUID, member_id: UUID, body
    ):
        await self._ensure_member_exists(access, member_id)
        return self._unwrap(
            await self.event_repository.update_player_status(
                access, event_id, member_id, body
            )
        )

    async def remove_player(self, access: AccessData, event_id: UUID, member_id: UUID):
        await self._ensure_member_exists(access, member_id)
        return self._unwrap(
            await self.event_repository.remove_player(access, event_id, member_id)
        )

    async def add_player(self, access: AccessData, event_id: UUID, body):
        await self._ensure_member_exists(access, body.member_id)
        if body.roles:
            game_role_ids = {r.game_role_id for r in body.roles}
            await self._ensure_game_roles_exist(access, game_role_ids)
        return self._unwrap(
            await self.event_repository.add_player(access, event_id, body)
        )

    async def update_player_roles(
        self, access: AccessData, event_id: UUID, member_id: UUID, body
    ):
        await self._ensure_member_exists(access, member_id)
        game_role_ids = {r.game_role_id for r in body.roles}
        await self._ensure_game_roles_exist(access, game_role_ids)
        return self._unwrap(
            await self.event_repository.update_player_roles(
                access, event_id, member_id, body
            )
        )

    async def create_draft(self, access: AccessData, event_id: UUID, body):
        return self._unwrap(
            await self.event_repository.create_draft(access, event_id, body)
        )

    async def get_draft(self, access: AccessData, draft_id: UUID):
        return self._unwrap(await self.event_repository.get_draft(access, draft_id))

    async def list_drafts(
        self, access: AccessData, event_id: UUID, page: int, page_size: int
    ):
        return self._unwrap(
            await self.event_repository.list_drafts(
                access, event_id, PaginationRequest(page=page, page_size=page_size)
            )
        )

    async def _get_drafted_players(self, access: AccessData, event_id: UUID, drafted_ids: set[UUID]):
        response = await self.event_repository.get_players_by_ids(
            access, event_id, list(drafted_ids)
        )
        return self._unwrap(response)

    async def _load_customs_for_players(self, access: AccessData, players):
        member_to_custom_ids: dict[UUID, set[UUID]] = {}
        for p in players:
            if p.custom_id:
                member_to_custom_ids.setdefault(p.member_id, set()).add(p.custom_id)

        custom_by_id: dict[UUID, InfraCustomResponse] = {}
        for member_id, custom_ids in member_to_custom_ids.items():
            response = await self.custom_repository.get_customs_by_member(
                access, member_id
            )
            if isinstance(response.message, ServerErrorResponse):
                continue
            for c in response.message:
                if c.id in custom_ids:
                    custom_by_id[c.id] = c
        return custom_by_id

    async def _build_rating_snapshot(self, access: AccessData, draft_id: UUID) -> list[RatingSnapshotInput]:
        draft = self._unwrap(await self.event_repository.get_draft(access, draft_id))

        drafted_ids = {dp.event_player_id for dp in draft.drafted_players}
        if not drafted_ids:
            return []

        players = await self._get_drafted_players(access, draft.event_id, drafted_ids)

        custom_by_id = await self._load_customs_for_players(access, players)

        snapshot: list[RatingSnapshotInput] = []
        for player in players:
            custom = custom_by_id.get(player.custom_id) if player.custom_id else None
            for role in player.roles:
                open_rating = 1000.0
                if custom:
                    for cr in custom.custom_ratings:
                        if cr.game_role.id == role.game_role_id:
                            open_rating = float(cr.rating)
                            break
                snapshot.append(RatingSnapshotInput(
                    member_id=player.member_id,
                    event_player_id=player.id,
                    game_role_id=role.game_role_id,
                    priority=role.priority,
                    open_rating=open_rating,
                ))
        return snapshot

    async def run_team_formation(self, access: AccessData, draft_id: UUID, body):
        rating_snapshot = await self._build_rating_snapshot(access, draft_id)
        await self._ensure_game_roles_exist(
            access, {item.game_role_id for item in rating_snapshot}
        )
        return self._unwrap(
            await self.event_repository.run_team_formation(
                access, draft_id, body, rating_snapshot
            )
        )

    async def get_team_formation(
        self, access: AccessData, draft_id: UUID, page: int, page_size: int
    ):
        return self._unwrap(
            await self.event_repository.get_team_formation(
                access, draft_id, PaginationRequest(page=page, page_size=page_size)
            )
        )

    async def choose_team_formation_variant(
        self, access: AccessData, draft_id: UUID, variant_id: UUID
    ):
        return self._unwrap(
            await self.event_repository.choose_team_formation_variant(
                access, draft_id, variant_id
            )
        )

    async def list_teams(
        self, access: AccessData, event_id: UUID, page: int, page_size: int
    ):
        return self._unwrap(
            await self.event_repository.list_teams(
                access, event_id, PaginationRequest(page=page, page_size=page_size)
            )
        )

    async def setup_match(self, access: AccessData, event_id: UUID, body):
        return self._unwrap(
            await self.event_repository.setup_match(access, event_id, body)
        )

    async def record_match_result(self, access: AccessData, match_id: UUID, body):
        return self._unwrap(
            await self.event_repository.record_match_result(access, match_id, body)
        )

    async def get_match(self, access: AccessData, match_id: UUID):
        return self._unwrap(await self.event_repository.get_match(access, match_id))

    async def list_matches(
        self,
        access: AccessData,
        event_id: UUID,
        active: bool | None,
        page: int,
        page_size: int,
    ):
        return self._unwrap(
            await self.event_repository.list_matches(
                access,
                event_id,
                active,
                PaginationRequest(page=page, page_size=page_size),
            )
        )

    async def add_integration(self, access: AccessData, event_id: UUID, name: str):
        return self._unwrap(
            await self.event_repository.add_integration(access, event_id, name)
        )

    async def remove_integration(self, access: AccessData, event_id: UUID, integration_id: UUID):
        return self._unwrap(
            await self.event_repository.remove_integration(access, event_id, integration_id)
        )

    async def add_game_role(
        self, access: AccessData, event_id: UUID, game_role_id: UUID,
        override_max_count: int | None, override_min_count: int | None
    ):
        await self._ensure_game_roles_exist(access, {game_role_id})
        return self._unwrap(
            await self.event_repository.add_game_role(
                access, event_id, game_role_id, override_max_count, override_min_count
            )
        )

    async def update_game_role(
        self, access: AccessData, event_id: UUID, selected_role_id: UUID,
        override_max_count: int | None, override_min_count: int | None
    ):
        return self._unwrap(
            await self.event_repository.update_game_role(
                access, event_id, selected_role_id, override_max_count, override_min_count
            )
        )

    async def remove_game_role(self, access: AccessData, event_id: UUID, selected_role_id: UUID):
        return self._unwrap(
            await self.event_repository.remove_game_role(access, event_id, selected_role_id)
        )

    async def add_custom_field(
        self, access: AccessData, event_id: UUID, name: str,
        is_private: bool, is_required: bool
    ):
        return self._unwrap(
            await self.event_repository.add_custom_field(
                access, event_id, name, is_private, is_required
            )
        )

    async def update_custom_field(
        self, access: AccessData, event_id: UUID, field_id: UUID,
        name: str | None, is_private: bool | None, is_required: bool | None
    ):
        return self._unwrap(
            await self.event_repository.update_custom_field(
                access, event_id, field_id, name, is_private, is_required
            )
        )

    async def remove_custom_field(self, access: AccessData, event_id: UUID, field_id: UUID):
        return self._unwrap(
            await self.event_repository.remove_custom_field(access, event_id, field_id)
        )

    async def update_time_settings(self, access: AccessData, event_id: UUID, body):
        return self._unwrap(
            await self.event_repository.update_time_settings(access, event_id, body)
        )

    async def list_events(
        self, server_id: UUID, access: AccessData
    ):
        return self._unwrap(
            await self.event_repository.list_events(server_id, access)
        )

    async def get_application_form_settings(self, event_id: UUID, access: AccessData):
        return self._unwrap(
            await self.event_repository.get_application_form_settings(event_id, access)
        )
