from uuid import UUID

from faststream.rabbit import RabbitBroker, RabbitMessage

from src.infra.communication.rpc import rpc_request
from pydantic import BaseModel

from src.domain.models.access import AccessData
from .models.request import (
    AccessDataRequest,
    ActivateEventRequest,
    AddOrganizerRequest,
    CancelEventRequest,
    ChooseTeamFormationVariantRequest,
    CloseRegistrationRequest,
    CompleteEventRequest,
    CreateDraftRequest,
    CreateEventRequest,
    GetApplicationRequest,
    GetDraftRequest,
    GetEventRequest,
    GetMatchRequest,
    GetTeamFormationRequest,
    HealthRequest,
    ListApplicationsRequest,
    ListDraftsRequest,
    ListEventsRequest,
    ListMatchesRequest,
    ListOrganizersRequest,
    ListPlayersRequest,
    ListTeamsRequest,
    OpenRegistrationRequest,
    PaginationRequest,
    RecordMatchResultRequest,
    RemoveOrganizerRequest,
    RemovePlayerRequest,
    ReviewApplicationRequest,
    RunTeamFormationRequest,
    SetupMatchRequest,
    SubmitApplicationRequest,
    UpdateEventRequest,
    UpdatePlayerStatusRequest,
)
from .models.response import (
    ErrorResponse,
    EventCard,
    EventDetail,
    RecordedMatchResult,
    ResponseMessage,
    SingleMatchView,
    StatusResponse,
    TeamFormationJob,
)


class MixerEventRepository:
    def __init__(self, broker: RabbitBroker):
        self.broker = broker

    def _access_data(self, access: AccessData) -> AccessDataRequest:
        return AccessDataRequest(
            member_id=access.member_id,
            server_id=access.server_id,
            permission_mask=access.permission_mask,
            restriction_mask=access.restriction_mask,
        )

    async def health(self) -> ResponseMessage[ErrorResponse | StatusResponse]:
        response: RabbitMessage = await rpc_request(self.broker, 
            HealthRequest(), queue="event.health"
        )
        return ResponseMessage[ErrorResponse | StatusResponse].model_validate_json(
            response.body
        )

    async def create_event(
        self,
        access: AccessData,
        body: BaseModel,
    ) -> ResponseMessage[ErrorResponse | EventCard]:
        request = CreateEventRequest(
            access_data=self._access_data(access), **body.model_dump()
        )
        response: RabbitMessage = await rpc_request(self.broker, 
            request, queue="event.create"
        )
        return ResponseMessage[ErrorResponse | EventCard].model_validate_json(
            response.body
        )

    async def get_event(
        self, access: AccessData, event_id: UUID
    ) -> ResponseMessage[ErrorResponse | EventCard | EventDetail]:
        request = GetEventRequest(event_id=event_id, access_data=self._access_data(access))
        response: RabbitMessage = await rpc_request(self.broker, request, queue="event.get")
        return ResponseMessage[
            ErrorResponse | EventCard | EventDetail
        ].model_validate_json(response.body)

    async def list_public_events(
        self, server_id: UUID, pagination: PaginationRequest
    ) -> ResponseMessage[ErrorResponse | list[EventCard]]:
        request = ListEventsRequest(server_id=server_id, pagination=pagination)
        response: RabbitMessage = await rpc_request(self.broker, 
            request, queue="event.list_public"
        )
        return ResponseMessage[ErrorResponse | list[EventCard]].model_validate_json(
            response.body
        )

    async def list_private_events(
        self, access: AccessData, pagination: PaginationRequest
    ) -> ResponseMessage[ErrorResponse | list[EventDetail]]:
        request = ListEventsRequest(
            access_data=self._access_data(access), pagination=pagination
        )
        response: RabbitMessage = await rpc_request(self.broker, 
            request, queue="event.list_private"
        )
        return ResponseMessage[ErrorResponse | list[EventDetail]].model_validate_json(
            response.body
        )

    async def update_event(
        self,
        access: AccessData,
        event_id: UUID,
        body: BaseModel,
    ) -> ResponseMessage[ErrorResponse | EventDetail]:
        request = UpdateEventRequest(
            access_data=self._access_data(access),
            event_id=event_id,
            **body.model_dump(exclude_unset=True),
        )
        response: RabbitMessage = await rpc_request(self.broker, 
            request, queue="event.update"
        )
        return ResponseMessage[ErrorResponse | EventDetail].model_validate_json(
            response.body
        )

    async def activate_event(
        self, access: AccessData, event_id: UUID
    ) -> ResponseMessage[ErrorResponse | EventDetail]:
        request = ActivateEventRequest(
            access_data=self._access_data(access), event_id=event_id
        )
        response: RabbitMessage = await rpc_request(self.broker, 
            request, queue="event.activate"
        )
        return ResponseMessage[ErrorResponse | EventDetail].model_validate_json(
            response.body
        )

    async def open_registration(
        self, access: AccessData, event_id: UUID
    ) -> ResponseMessage[ErrorResponse | EventDetail]:
        request = OpenRegistrationRequest(
            access_data=self._access_data(access), event_id=event_id
        )
        response: RabbitMessage = await rpc_request(self.broker, 
            request, queue="event.registration.open"
        )
        return ResponseMessage[ErrorResponse | EventDetail].model_validate_json(
            response.body
        )

    async def close_registration(
        self, access: AccessData, event_id: UUID
    ) -> ResponseMessage[ErrorResponse | EventDetail]:
        request = CloseRegistrationRequest(
            access_data=self._access_data(access), event_id=event_id
        )
        response: RabbitMessage = await rpc_request(self.broker, 
            request, queue="event.registration.close"
        )
        return ResponseMessage[ErrorResponse | EventDetail].model_validate_json(
            response.body
        )

    async def cancel_event(
        self, access: AccessData, event_id: UUID
    ) -> ResponseMessage[ErrorResponse | EventDetail]:
        request = CancelEventRequest(
            access_data=self._access_data(access), event_id=event_id
        )
        response: RabbitMessage = await rpc_request(self.broker, request, queue="event.cancel")
        return ResponseMessage[ErrorResponse | EventDetail].model_validate_json(
            response.body
        )

    async def complete_event(
        self, access: AccessData, event_id: UUID
    ) -> ResponseMessage[ErrorResponse | EventDetail]:
        request = CompleteEventRequest(
            access_data=self._access_data(access), event_id=event_id
        )
        response: RabbitMessage = await rpc_request(self.broker, 
            request, queue="event.complete"
        )
        return ResponseMessage[ErrorResponse | EventDetail].model_validate_json(
            response.body
        )

    async def list_organizers(
        self, access: AccessData, event_id: UUID, pagination: PaginationRequest
    ) -> ResponseMessage[ErrorResponse | list[dict]]:
        request = ListOrganizersRequest(
            event_id=event_id,
            access_data=self._access_data(access),
            pagination=pagination,
        )
        response: RabbitMessage = await rpc_request(self.broker, 
            request, queue="event.organizer.list"
        )
        return ResponseMessage[ErrorResponse | list[dict]].model_validate_json(
            response.body
        )

    async def add_organizer(
        self, access: AccessData, event_id: UUID, member_id: UUID
    ) -> ResponseMessage[ErrorResponse | dict]:
        request = AddOrganizerRequest(
            access_data=self._access_data(access),
            event_id=event_id,
            member_id=member_id,
        )
        response: RabbitMessage = await rpc_request(self.broker, 
            request, queue="event.organizer.add"
        )
        return ResponseMessage[ErrorResponse | dict].model_validate_json(response.body)

    async def remove_organizer(
        self, access: AccessData, event_id: UUID, member_id: UUID
    ) -> ResponseMessage[ErrorResponse | StatusResponse]:
        request = RemoveOrganizerRequest(
            access_data=self._access_data(access),
            event_id=event_id,
            member_id=member_id,
        )
        response: RabbitMessage = await rpc_request(self.broker, 
            request, queue="event.organizer.remove"
        )
        return ResponseMessage[ErrorResponse | StatusResponse].model_validate_json(
            response.body
        )

    async def submit_application(
        self,
        access: AccessData,
        event_id: UUID,
        body: BaseModel,
    ) -> ResponseMessage[ErrorResponse | dict]:
        request = SubmitApplicationRequest(
            access_data=self._access_data(access), event_id=event_id, **body.model_dump()
        )
        response: RabbitMessage = await rpc_request(self.broker, 
            request, queue="event.application.submit"
        )
        return ResponseMessage[ErrorResponse | dict].model_validate_json(response.body)

    async def get_application(
        self, access: AccessData, application_id: UUID
    ) -> ResponseMessage[ErrorResponse | dict]:
        request = GetApplicationRequest(
            application_id=application_id, access_data=self._access_data(access)
        )
        response: RabbitMessage = await rpc_request(self.broker, 
            request, queue="event.application.get"
        )
        return ResponseMessage[ErrorResponse | dict].model_validate_json(response.body)

    async def list_applications(
        self,
        access: AccessData,
        event_id: UUID,
        status: str | None,
        pagination: PaginationRequest,
    ) -> ResponseMessage[ErrorResponse | list[dict]]:
        request = ListApplicationsRequest(
            event_id=event_id,
            access_data=self._access_data(access),
            status=status,
            pagination=pagination,
        )
        response: RabbitMessage = await rpc_request(self.broker, 
            request, queue="event.application.list"
        )
        return ResponseMessage[ErrorResponse | list[dict]].model_validate_json(
            response.body
        )

    async def review_application(
        self,
        access: AccessData,
        application_id: UUID,
        body: BaseModel,
    ) -> ResponseMessage[ErrorResponse | dict]:
        request = ReviewApplicationRequest(
            access_data=self._access_data(access),
            application_id=application_id,
            **body.model_dump(),
        )
        response: RabbitMessage = await rpc_request(self.broker, 
            request, queue="event.application.review"
        )
        return ResponseMessage[ErrorResponse | dict].model_validate_json(response.body)

    async def list_players(
        self,
        access: AccessData,
        event_id: UUID,
        status: str | None,
        pagination: PaginationRequest,
    ) -> ResponseMessage[ErrorResponse | list[dict]]:
        request = ListPlayersRequest(
            event_id=event_id,
            access_data=self._access_data(access),
            status=status,
            pagination=pagination,
        )
        response: RabbitMessage = await rpc_request(self.broker, 
            request, queue="event.player.list"
        )
        return ResponseMessage[ErrorResponse | list[dict]].model_validate_json(
            response.body
        )

    async def update_player_status(
        self,
        access: AccessData,
        event_id: UUID,
        member_id: UUID,
        body: BaseModel,
    ) -> ResponseMessage[ErrorResponse | dict]:
        request = UpdatePlayerStatusRequest(
            access_data=self._access_data(access),
            event_id=event_id,
            member_id=member_id,
            **body.model_dump(),
        )
        response: RabbitMessage = await rpc_request(self.broker, 
            request, queue="event.player.status.update"
        )
        return ResponseMessage[ErrorResponse | dict].model_validate_json(response.body)

    async def remove_player(
        self, access: AccessData, event_id: UUID, member_id: UUID
    ) -> ResponseMessage[ErrorResponse | StatusResponse]:
        request = RemovePlayerRequest(
            access_data=self._access_data(access),
            event_id=event_id,
            member_id=member_id,
        )
        response: RabbitMessage = await rpc_request(self.broker, 
            request, queue="event.player.remove"
        )
        return ResponseMessage[ErrorResponse | StatusResponse].model_validate_json(
            response.body
        )

    async def create_draft(
        self, access: AccessData, event_id: UUID, body: BaseModel
    ) -> ResponseMessage[ErrorResponse | dict]:
        request = CreateDraftRequest(
            access_data=self._access_data(access), event_id=event_id, **body.model_dump()
        )
        response: RabbitMessage = await rpc_request(self.broker, 
            request, queue="event.draft.create"
        )
        return ResponseMessage[ErrorResponse | dict].model_validate_json(response.body)

    async def get_draft(
        self, access: AccessData, draft_id: UUID
    ) -> ResponseMessage[ErrorResponse | dict]:
        request = GetDraftRequest(draft_id=draft_id, access_data=self._access_data(access))
        response: RabbitMessage = await rpc_request(self.broker, 
            request, queue="event.draft.get"
        )
        return ResponseMessage[ErrorResponse | dict].model_validate_json(response.body)

    async def list_drafts(
        self, access: AccessData, event_id: UUID, pagination: PaginationRequest
    ) -> ResponseMessage[ErrorResponse | list[dict]]:
        request = ListDraftsRequest(
            event_id=event_id,
            access_data=self._access_data(access),
            pagination=pagination,
        )
        response: RabbitMessage = await rpc_request(self.broker, 
            request, queue="event.draft.list"
        )
        return ResponseMessage[ErrorResponse | list[dict]].model_validate_json(
            response.body
        )

    async def run_team_formation(
        self, access: AccessData, draft_id: UUID, body: BaseModel
    ) -> ResponseMessage[ErrorResponse | TeamFormationJob]:
        request = RunTeamFormationRequest(
            access_data=self._access_data(access), draft_id=draft_id, **body.model_dump()
        )
        response: RabbitMessage = await rpc_request(self.broker, 
            request, queue="event.team_formation.run"
        )
        return ResponseMessage[ErrorResponse | TeamFormationJob].model_validate_json(
            response.body
        )

    async def get_team_formation(
        self, access: AccessData, draft_id: UUID, pagination: PaginationRequest
    ) -> ResponseMessage[ErrorResponse | TeamFormationJob]:
        request = GetTeamFormationRequest(
            draft_id=draft_id,
            access_data=self._access_data(access),
            pagination=pagination,
        )
        response: RabbitMessage = await rpc_request(self.broker, 
            request, queue="event.team_formation.get"
        )
        return ResponseMessage[ErrorResponse | TeamFormationJob].model_validate_json(
            response.body
        )

    async def choose_team_formation_variant(
        self, access: AccessData, draft_id: UUID, variant_id: UUID
    ) -> ResponseMessage[ErrorResponse | dict]:
        request = ChooseTeamFormationVariantRequest(
            access_data=self._access_data(access),
            draft_id=draft_id,
            variant_id=variant_id,
        )
        response: RabbitMessage = await rpc_request(self.broker, 
            request, queue="event.team_formation.choose"
        )
        return ResponseMessage[ErrorResponse | dict].model_validate_json(response.body)

    async def list_teams(
        self, access: AccessData, event_id: UUID, pagination: PaginationRequest
    ) -> ResponseMessage[ErrorResponse | list[dict]]:
        request = ListTeamsRequest(
            event_id=event_id,
            access_data=self._access_data(access),
            pagination=pagination,
        )
        response: RabbitMessage = await rpc_request(self.broker, 
            request, queue="event.team.list"
        )
        return ResponseMessage[ErrorResponse | list[dict]].model_validate_json(
            response.body
        )

    async def setup_match(
        self, access: AccessData, event_id: UUID, body: BaseModel
    ) -> ResponseMessage[ErrorResponse | SingleMatchView]:
        request = SetupMatchRequest(
            access_data=self._access_data(access), event_id=event_id, **body.model_dump()
        )
        response: RabbitMessage = await rpc_request(self.broker, 
            request, queue="event.match.setup"
        )
        return ResponseMessage[ErrorResponse | SingleMatchView].model_validate_json(
            response.body
        )

    async def record_match_result(
        self, access: AccessData, match_id: UUID, body: BaseModel
    ) -> ResponseMessage[ErrorResponse | RecordedMatchResult]:
        request = RecordMatchResultRequest(
            access_data=self._access_data(access), match_id=match_id, **body.model_dump()
        )
        response: RabbitMessage = await rpc_request(self.broker, 
            request, queue="event.match.result.record"
        )
        return ResponseMessage[
            ErrorResponse | RecordedMatchResult
        ].model_validate_json(response.body)

    async def get_match(
        self, access: AccessData, match_id: UUID
    ) -> ResponseMessage[ErrorResponse | SingleMatchView]:
        request = GetMatchRequest(match_id=match_id, access_data=self._access_data(access))
        response: RabbitMessage = await rpc_request(self.broker, 
            request, queue="event.match.get"
        )
        return ResponseMessage[ErrorResponse | SingleMatchView].model_validate_json(
            response.body
        )

    async def list_matches(
        self,
        access: AccessData,
        event_id: UUID,
        active: bool | None,
        pagination: PaginationRequest,
    ) -> ResponseMessage[ErrorResponse | list[SingleMatchView]]:
        request = ListMatchesRequest(
            event_id=event_id,
            access_data=self._access_data(access),
            active=active,
            pagination=pagination,
        )
        response: RabbitMessage = await rpc_request(self.broker, 
            request, queue="event.match.list"
        )
        return ResponseMessage[
            ErrorResponse | list[SingleMatchView]
        ].model_validate_json(response.body)
