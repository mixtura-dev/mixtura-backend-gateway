from uuid import UUID

from src.infra.communication.rabbit import RabbitRpcClient
from src.infra.communication.rpc import rpc_request
from pydantic import BaseModel

from src.domain.models.access import AccessData
from .models.request import (
    AccessDataRequest,
    ActivateEventRequest,
    AddOrganizerRequest,
    AddIntegrationRequest,
    AddPlayerRequest,
    RemoveIntegrationRequest,
    AddGameRoleRequest,
    UpdateGameRoleRequest,
    RemoveGameRoleRequest,
    AddCustomFieldRequest,
    UpdateCustomFieldRequest,
    RemoveCustomFieldRequest,
    UpdatePlayerRolesRequest,
    UpdateTimeSettingsRequest,
    ListEventsUnifiedRequest,
    GetApplicationFormSettingsRequest,
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
    ApplicationDetail,
    ApplicationFormSettings,
    ApplicationListItem,
    ApplicationReviewResult,
    ApplicationSubmitResult,
    DraftDetail,
    DraftItem,
    ErrorResponse,
    EventCard,
    EventDetail,
    OrganizerItem,
    PlayerItem,
    PlayerUpdateResult,
    ResponseMessage,
    SingleMatchView,
    StatusResponse,
    TeamDetail,
    TeamFormationJob,
    TeamItem,
)


class MixerEventRepository:
    def __init__(self, rpc_client: RabbitRpcClient):
        self.rpc_client = rpc_client

    def _access_data(self, access: AccessData) -> AccessDataRequest:
        return AccessDataRequest(
            member_id=access.member_id,
            server_id=access.server_id,
            permission_mask=access.permission_mask,
            restriction_mask=access.restriction_mask,
        )

    async def health(self) -> ResponseMessage[ErrorResponse | StatusResponse]:
        response = await rpc_request(self.rpc_client,
            HealthRequest(), queue="event.health"
        )
        return ResponseMessage[ErrorResponse | StatusResponse].model_validate_json(
            response.body
        )

    async def create_event(
        self,
        access: AccessData,
        body: BaseModel,
        rating_set_id: UUID,
    ) -> ResponseMessage[ErrorResponse | EventDetail]:
        data = body.model_dump()
        data["rating_set_id"] = rating_set_id
        request = CreateEventRequest(
            access_data=self._access_data(access), **data
        )
        response = await rpc_request(self.rpc_client,
            request, queue="event.create"
        )
        return ResponseMessage[ErrorResponse | EventDetail].model_validate_json(
            response.body
        )

    async def get_event(
        self, access: AccessData, event_id: UUID
    ) -> ResponseMessage[ErrorResponse | EventDetail]:
        request = GetEventRequest(event_id=event_id, access_data=self._access_data(access))
        response = await rpc_request(self.rpc_client, request, queue="event.get")
        return ResponseMessage[
            ErrorResponse | EventDetail
        ].model_validate_json(response.body)

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
        response = await rpc_request(self.rpc_client,
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
        response = await rpc_request(self.rpc_client,
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
        response = await rpc_request(self.rpc_client,
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
        response = await rpc_request(self.rpc_client,
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
        response = await rpc_request(self.rpc_client, request, queue="event.cancel")
        return ResponseMessage[ErrorResponse | EventDetail].model_validate_json(
            response.body
        )

    async def complete_event(
        self, access: AccessData, event_id: UUID
    ) -> ResponseMessage[ErrorResponse | EventDetail]:
        request = CompleteEventRequest(
            access_data=self._access_data(access), event_id=event_id
        )
        response = await rpc_request(self.rpc_client,
            request, queue="event.complete"
        )
        return ResponseMessage[ErrorResponse | EventDetail].model_validate_json(
            response.body
        )

    async def list_organizers(
        self, access: AccessData, event_id: UUID, pagination: PaginationRequest
    ) -> ResponseMessage[ErrorResponse | list[OrganizerItem]]:
        request = ListOrganizersRequest(
            event_id=event_id,
            access_data=self._access_data(access),
            pagination=pagination,
        )
        response = await rpc_request(self.rpc_client,
            request, queue="event.organizer.list"
        )
        return ResponseMessage[ErrorResponse | list[OrganizerItem]].model_validate_json(
            response.body
        )

    async def add_organizer(
        self, access: AccessData, event_id: UUID, member_id: UUID
    ) -> ResponseMessage[ErrorResponse | OrganizerItem]:
        request = AddOrganizerRequest(
            access_data=self._access_data(access),
            event_id=event_id,
            member_id=member_id,
        )
        response = await rpc_request(self.rpc_client,
            request, queue="event.organizer.add"
        )
        return ResponseMessage[ErrorResponse | OrganizerItem].model_validate_json(response.body)

    async def remove_organizer(
        self, access: AccessData, event_id: UUID, member_id: UUID
    ) -> ResponseMessage[ErrorResponse | StatusResponse]:
        request = RemoveOrganizerRequest(
            access_data=self._access_data(access),
            event_id=event_id,
            member_id=member_id,
        )
        response = await rpc_request(self.rpc_client,
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
        integrations: list[dict[str, object]] | None = None,
    ) -> ResponseMessage[ErrorResponse | ApplicationSubmitResult]:
        data = body.model_dump()
        if integrations is not None:
            data["integrations"] = integrations
        request = SubmitApplicationRequest(
            access_data=self._access_data(access), event_id=event_id, **data
        )
        response = await rpc_request(self.rpc_client,
            request, queue="event.application.submit"
        )
        return ResponseMessage[ErrorResponse | ApplicationSubmitResult].model_validate_json(response.body)

    async def get_application(
        self, access: AccessData, application_id: UUID
    ) -> ResponseMessage[ErrorResponse | ApplicationDetail]:
        request = GetApplicationRequest(
            application_id=application_id, access_data=self._access_data(access)
        )
        response = await rpc_request(self.rpc_client,
            request, queue="event.application.get"
        )
        return ResponseMessage[ErrorResponse | ApplicationDetail].model_validate_json(response.body)

    async def list_applications(
        self,
        access: AccessData,
        event_id: UUID,
        status: str | None,
        pagination: PaginationRequest,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ) -> ResponseMessage[ErrorResponse | list[ApplicationListItem]]:
        request = ListApplicationsRequest(
            event_id=event_id,
            access_data=self._access_data(access),
            status=status,
            pagination=pagination,
            sort_by=sort_by,
            sort_order=sort_order,
        )
        response = await rpc_request(self.rpc_client,
            request, queue="event.application.list"
        )
        return ResponseMessage[ErrorResponse | list[ApplicationListItem]].model_validate_json(
            response.body
        )

    async def review_application(
        self,
        access: AccessData,
        application_id: UUID,
        body: BaseModel,
    ) -> ResponseMessage[ErrorResponse | ApplicationReviewResult]:
        request = ReviewApplicationRequest(
            access_data=self._access_data(access),
            application_id=application_id,
            **body.model_dump(),
        )
        response = await rpc_request(self.rpc_client,
            request, queue="event.application.review"
        )
        return ResponseMessage[ErrorResponse | ApplicationReviewResult].model_validate_json(response.body)

    async def list_players(
        self,
        access: AccessData,
        event_id: UUID,
        status: str | None,
        pagination: PaginationRequest,
    ) -> ResponseMessage[ErrorResponse | list[PlayerItem]]:
        request = ListPlayersRequest(
            event_id=event_id,
            access_data=self._access_data(access),
            status=status,
            pagination=pagination,
        )
        response = await rpc_request(self.rpc_client,
            request, queue="event.player.list"
        )
        return ResponseMessage[ErrorResponse | list[PlayerItem]].model_validate_json(
            response.body
        )

    async def update_player_status(
        self,
        access: AccessData,
        event_id: UUID,
        member_id: UUID,
        body: BaseModel,
    ) -> ResponseMessage[ErrorResponse | PlayerUpdateResult]:
        request = UpdatePlayerStatusRequest(
            access_data=self._access_data(access),
            event_id=event_id,
            member_id=member_id,
            **body.model_dump(),
        )
        response = await rpc_request(self.rpc_client,
            request, queue="event.player.status.update"
        )
        return ResponseMessage[ErrorResponse | PlayerUpdateResult].model_validate_json(response.body)

    async def remove_player(
        self, access: AccessData, event_id: UUID, member_id: UUID
    ) -> ResponseMessage[ErrorResponse | StatusResponse]:
        request = RemovePlayerRequest(
            access_data=self._access_data(access),
            event_id=event_id,
            member_id=member_id,
        )
        response = await rpc_request(self.rpc_client,
            request, queue="event.player.remove"
        )
        return ResponseMessage[ErrorResponse | StatusResponse].model_validate_json(
            response.body
        )

    async def add_player(
        self, access: AccessData, event_id: UUID, body: BaseModel
    ) -> ResponseMessage[ErrorResponse | PlayerItem]:
        request = AddPlayerRequest(
            access_data=self._access_data(access),
            event_id=event_id,
            **body.model_dump(),
        )
        response = await rpc_request(self.rpc_client,
            request, queue="event.player.add"
        )
        return ResponseMessage[ErrorResponse | PlayerItem].model_validate_json(response.body)

    async def update_player_roles(
        self, access: AccessData, event_id: UUID, member_id: UUID, body: BaseModel
    ) -> ResponseMessage[ErrorResponse | PlayerItem]:
        request = UpdatePlayerRolesRequest(
            access_data=self._access_data(access),
            event_id=event_id,
            member_id=member_id,
            **body.model_dump(),
        )
        response = await rpc_request(self.rpc_client,
            request, queue="event.player.roles.update"
        )
        return ResponseMessage[ErrorResponse | PlayerItem].model_validate_json(response.body)

    async def create_draft(
        self, access: AccessData, event_id: UUID, body: BaseModel
    ) -> ResponseMessage[ErrorResponse | DraftDetail]:
        request = CreateDraftRequest(
            access_data=self._access_data(access), event_id=event_id, **body.model_dump()
        )
        response = await rpc_request(self.rpc_client,
            request, queue="event.draft.create"
        )
        return ResponseMessage[ErrorResponse | DraftDetail].model_validate_json(response.body)

    async def get_draft(
        self, access: AccessData, draft_id: UUID
    ) -> ResponseMessage[ErrorResponse | DraftDetail]:
        request = GetDraftRequest(draft_id=draft_id, access_data=self._access_data(access))
        response = await rpc_request(self.rpc_client,
            request, queue="event.draft.get"
        )
        return ResponseMessage[ErrorResponse | DraftDetail].model_validate_json(response.body)

    async def list_drafts(
        self, access: AccessData, event_id: UUID, pagination: PaginationRequest
    ) -> ResponseMessage[ErrorResponse | list[DraftItem]]:
        request = ListDraftsRequest(
            event_id=event_id,
            access_data=self._access_data(access),
            pagination=pagination,
        )
        response = await rpc_request(self.rpc_client,
            request, queue="event.draft.list"
        )
        return ResponseMessage[ErrorResponse | list[DraftItem]].model_validate_json(
            response.body
        )

    async def run_team_formation(
        self, access: AccessData, draft_id: UUID, body: BaseModel
    ) -> ResponseMessage[ErrorResponse | TeamFormationJob]:
        request = RunTeamFormationRequest(
            access_data=self._access_data(access), draft_id=draft_id, **body.model_dump()
        )
        response = await rpc_request(self.rpc_client,
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
        response = await rpc_request(self.rpc_client,
            request, queue="event.team_formation.get"
        )
        return ResponseMessage[ErrorResponse | TeamFormationJob].model_validate_json(
            response.body
        )

    async def choose_team_formation_variant(
        self, access: AccessData, draft_id: UUID, variant_id: UUID
    ) -> ResponseMessage[ErrorResponse | list[TeamDetail]]:
        request = ChooseTeamFormationVariantRequest(
            access_data=self._access_data(access),
            draft_id=draft_id,
            variant_id=variant_id,
        )
        response = await rpc_request(self.rpc_client,
            request, queue="event.team_formation.choose"
        )
        return ResponseMessage[ErrorResponse | list[TeamDetail]].model_validate_json(response.body)

    async def list_teams(
        self, access: AccessData, event_id: UUID, pagination: PaginationRequest
    ) -> ResponseMessage[ErrorResponse | list[TeamItem]]:
        request = ListTeamsRequest(
            event_id=event_id,
            access_data=self._access_data(access),
            pagination=pagination,
        )
        response = await rpc_request(self.rpc_client,
            request, queue="event.team.list"
        )
        return ResponseMessage[ErrorResponse | list[TeamItem]].model_validate_json(
            response.body
        )

    async def setup_match(
        self, access: AccessData, event_id: UUID, body: BaseModel
    ) -> ResponseMessage[ErrorResponse | SingleMatchView]:
        request = SetupMatchRequest(
            access_data=self._access_data(access), event_id=event_id, **body.model_dump()
        )
        response = await rpc_request(self.rpc_client,
            request, queue="event.match.setup"
        )
        return ResponseMessage[ErrorResponse | SingleMatchView].model_validate_json(
            response.body
        )

    async def record_match_result(
        self, access: AccessData, match_id: UUID, body: BaseModel
    ) -> ResponseMessage[ErrorResponse | SingleMatchView]:
        request = RecordMatchResultRequest(
            access_data=self._access_data(access), match_id=match_id, **body.model_dump()
        )
        response = await rpc_request(self.rpc_client,
            request, queue="event.match.result.record"
        )
        return ResponseMessage[
            ErrorResponse | SingleMatchView
        ].model_validate_json(response.body)

    async def get_match(
        self, access: AccessData, match_id: UUID
    ) -> ResponseMessage[ErrorResponse | SingleMatchView]:
        request = GetMatchRequest(match_id=match_id, access_data=self._access_data(access))
        response = await rpc_request(self.rpc_client,
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
        response = await rpc_request(self.rpc_client,
            request, queue="event.match.list"
        )
        return ResponseMessage[
            ErrorResponse | list[SingleMatchView]
        ].model_validate_json(response.body)

    async def add_integration(
        self, access: AccessData, event_id: UUID, name: str
    ) -> ResponseMessage[ErrorResponse | EventDetail]:
        request = AddIntegrationRequest(
            access_data=self._access_data(access), event_id=event_id, name=name
        )
        response = await rpc_request(self.rpc_client,
            request, queue="event.settings.integration.add"
        )
        return ResponseMessage[ErrorResponse | EventDetail].model_validate_json(response.body)

    async def remove_integration(
        self, access: AccessData, event_id: UUID, integration_id: UUID
    ) -> ResponseMessage[ErrorResponse | EventDetail]:
        request = RemoveIntegrationRequest(
            access_data=self._access_data(access), event_id=event_id, integration_id=integration_id
        )
        response = await rpc_request(self.rpc_client,
            request, queue="event.settings.integration.remove"
        )
        return ResponseMessage[ErrorResponse | EventDetail].model_validate_json(response.body)

    async def add_game_role(
        self, access: AccessData, event_id: UUID, game_role_id: UUID,
        override_max_count: int | None, override_min_count: int | None
    ) -> ResponseMessage[ErrorResponse | EventDetail]:
        request = AddGameRoleRequest(
            access_data=self._access_data(access),
            event_id=event_id,
            game_role_id=game_role_id,
            override_max_count=override_max_count,
            override_min_count=override_min_count,
        )
        response = await rpc_request(self.rpc_client,
            request, queue="event.settings.roles.add"
        )
        return ResponseMessage[ErrorResponse | EventDetail].model_validate_json(response.body)

    async def update_game_role(
        self, access: AccessData, event_id: UUID, selected_role_id: UUID,
        override_max_count: int | None, override_min_count: int | None
    ) -> ResponseMessage[ErrorResponse | EventDetail]:
        request = UpdateGameRoleRequest(
            access_data=self._access_data(access),
            event_id=event_id,
            selected_role_id=selected_role_id,
            override_max_count=override_max_count,
            override_min_count=override_min_count,
        )
        response = await rpc_request(self.rpc_client,
            request, queue="event.settings.roles.update"
        )
        return ResponseMessage[ErrorResponse | EventDetail].model_validate_json(response.body)

    async def remove_game_role(
        self, access: AccessData, event_id: UUID, selected_role_id: UUID
    ) -> ResponseMessage[ErrorResponse | EventDetail]:
        request = RemoveGameRoleRequest(
            access_data=self._access_data(access), event_id=event_id, selected_role_id=selected_role_id
        )
        response = await rpc_request(self.rpc_client,
            request, queue="event.settings.roles.remove"
        )
        return ResponseMessage[ErrorResponse | EventDetail].model_validate_json(response.body)

    async def add_custom_field(
        self, access: AccessData, event_id: UUID, name: str,
        is_private: bool, is_required: bool
    ) -> ResponseMessage[ErrorResponse | EventDetail]:
        request = AddCustomFieldRequest(
            access_data=self._access_data(access),
            event_id=event_id,
            name=name,
            is_private=is_private,
            is_required=is_required,
        )
        response = await rpc_request(self.rpc_client,
            request, queue="event.settings.custom_fields.add"
        )
        return ResponseMessage[ErrorResponse | EventDetail].model_validate_json(response.body)

    async def update_custom_field(
        self, access: AccessData, event_id: UUID, field_id: UUID,
        name: str | None, is_private: bool | None, is_required: bool | None
    ) -> ResponseMessage[ErrorResponse | EventDetail]:
        request = UpdateCustomFieldRequest(
            access_data=self._access_data(access),
            event_id=event_id,
            field_id=field_id,
            name=name,
            is_private=is_private,
            is_required=is_required,
        )
        response = await rpc_request(self.rpc_client,
            request, queue="event.settings.custom_fields.update"
        )
        return ResponseMessage[ErrorResponse | EventDetail].model_validate_json(response.body)

    async def remove_custom_field(
        self, access: AccessData, event_id: UUID, field_id: UUID
    ) -> ResponseMessage[ErrorResponse | EventDetail]:
        request = RemoveCustomFieldRequest(
            access_data=self._access_data(access), event_id=event_id, field_id=field_id
        )
        response = await rpc_request(self.rpc_client,
            request, queue="event.settings.custom_fields.remove"
        )
        return ResponseMessage[ErrorResponse | EventDetail].model_validate_json(response.body)

    async def update_time_settings(
        self, access: AccessData, event_id: UUID, body: BaseModel
    ) -> ResponseMessage[ErrorResponse | EventDetail]:
        request = UpdateTimeSettingsRequest(
            access_data=self._access_data(access), event_id=event_id, **body.model_dump(exclude_unset=True)
        )
        response = await rpc_request(self.rpc_client,
            request, queue="event.settings.time_settings.update"
        )
        return ResponseMessage[ErrorResponse | EventDetail].model_validate_json(response.body)

    async def list_events(
        self, server_id: UUID, access: AccessData
    ) -> ResponseMessage[ErrorResponse | list[EventCard]]:
        request = ListEventsUnifiedRequest(
            server_id=server_id,
            access_data=self._access_data(access),
        )
        response = await rpc_request(self.rpc_client,
            request, queue="event.list"
        )
        return ResponseMessage[ErrorResponse | list[EventCard]].model_validate_json(response.body)

    async def get_application_form_settings(
        self, event_id: UUID, access: AccessData
    ) -> ResponseMessage[ErrorResponse | ApplicationFormSettings]:
        request = GetApplicationFormSettingsRequest(
            event_id=event_id,
            access_data=self._access_data(access),
        )
        response = await rpc_request(self.rpc_client,
            request, queue="event.application.form_settings"
        )
        return ResponseMessage[ErrorResponse | ApplicationFormSettings].model_validate_json(response.body)
