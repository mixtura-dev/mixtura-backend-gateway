from uuid import UUID

from src.domain.exceptions import ServiceException
from src.domain.models.access import AccessData
from src.infra.communication.mixer.models.request import PaginationRequest
from src.infra.communication.mixer.models.response import ErrorResponse
from src.infra.communication.mixer.repository import MixerEventRepository


class MixerEventService:
    def __init__(self, event_repository: MixerEventRepository) -> None:
        self.event_repository = event_repository

    def _unwrap(self, response):
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message

    async def health(self):
        return self._unwrap(await self.event_repository.health())

    async def create_event(self, access: AccessData, body):
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
        return self._unwrap(
            await self.event_repository.update_player_status(
                access, event_id, member_id, body
            )
        )

    async def remove_player(self, access: AccessData, event_id: UUID, member_id: UUID):
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
