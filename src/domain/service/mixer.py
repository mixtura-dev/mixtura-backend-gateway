from uuid import UUID

from src.domain.exceptions import ServiceException
from src.domain.models.access import AccessData
from src.infra.communication.mixer.models.request import PaginationRequest
from src.infra.communication.mixer.models.response import ErrorResponse
from src.infra.communication.mixer.repository import MixerEventRepository
from src.infra.communication.server.repository.game_roles import GameRoleRepository
from src.infra.communication.server.repository.member import MemberRepository
from src.infra.communication.server.models.response import ErrorResponse as ServerErrorResponse
from src.infra.communication.server.repository.rating import RatingRepository


class MixerEventService:
    def __init__(
        self,
        event_repository: MixerEventRepository,
        rating_repository: RatingRepository,
        member_repository: MemberRepository,
        game_role_repository: GameRoleRepository,
    ) -> None:
        self.event_repository = event_repository
        self.rating_repository = rating_repository
        self.member_repository = member_repository
        self.game_role_repository = game_role_repository

    def _unwrap(self, response):
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message

    async def _ensure_rating_set_exists(
        self, access: AccessData, rating_set_id: UUID | None
    ) -> None:
        if rating_set_id is None:
            return

        response = await self.rating_repository.get_rating_set(access)
        if isinstance(response.message, ServerErrorResponse):
            raise ServiceException(response.status, response.message.message)
        if response.message.id != rating_set_id:
            raise ServiceException(404, "Rating set not found for server")

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
        await self._ensure_rating_set_exists(access, body.rating_set_id)
        return self._unwrap(await self.event_repository.create_event(access, body))

    async def get_event(self, access: AccessData, event_id: UUID):
        return self._unwrap(await self.event_repository.get_event(access, event_id))

    async def list_public_events(self, server_id: UUID, page: int, page_size: int):
        return self._unwrap(
            await self.event_repository.list_public_events(
                server_id, PaginationRequest(page=page, page_size=page_size)
            )
        )

    async def list_private_events(
        self, access: AccessData, page: int, page_size: int
    ):
        return self._unwrap(
            await self.event_repository.list_private_events(
                access, PaginationRequest(page=page, page_size=page_size)
            )
        )

    async def update_event(self, access: AccessData, event_id: UUID, body):
        await self._ensure_rating_set_exists(access, body.rating_set_id)
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

    async def submit_application(self, access: AccessData, event_id: UUID, body):
        await self._ensure_game_roles_exist(access, set(body.role_priorities))
        return self._unwrap(
            await self.event_repository.submit_application(access, event_id, body)
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
    ):
        return self._unwrap(
            await self.event_repository.list_applications(
                access,
                event_id,
                status,
                PaginationRequest(page=page, page_size=page_size),
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

    async def run_team_formation(self, access: AccessData, draft_id: UUID, body):
        await self._ensure_game_roles_exist(
            access, {item.game_role_id for item in body.rating_snapshot}
        )
        return self._unwrap(
            await self.event_repository.run_team_formation(access, draft_id, body)
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
