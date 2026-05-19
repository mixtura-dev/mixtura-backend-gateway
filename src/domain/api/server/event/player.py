from uuid import UUID

from fastapi import APIRouter

from src.dependency import (
    AuthorizedUserID,
    MemberCustomServiceDependency,
    MemberServiceDependency,
    MixerEventServiceDependency,
    PaginationDependency,
    RemapperServiceDependency,
)
from src.domain.models.mixer.enums import EventPlayerStatus
from src.domain.models.mixer.requests import (
    AddPlayerRequest,
    UpdatePlayerRolesRequest,
    UpdatePlayerStatusRequest,
)
from src.domain.models.mixer.responses import (
    EventPlayerResponse,
    PlayerUpdateResultResponse,
)
from src.domain.models.response import StatusResponse
from src.domain.models.server.custom.response import CustomResponse
from src.domain.models.server.member.response import ReducedMemberResponse

from ._utils import get_access

router = APIRouter(tags=["Event Player"])


@router.get("/{event_id}/players", response_model=list[EventPlayerResponse])
async def list_players(
    user_id: AuthorizedUserID,
    server_id: UUID,
    event_id: UUID,
    event_service: MixerEventServiceDependency,
    member_service: MemberServiceDependency,
    custom_service: MemberCustomServiceDependency,
    remapper_service: RemapperServiceDependency,
    pagination: PaginationDependency,
    status: EventPlayerStatus | None = None,
):
    access = await get_access(server_id, user_id, member_service)
    players = await event_service.list_players(
        access, event_id, status, pagination.page, pagination.page_size
    )

    unique_member_ids = {p.member_id for p in players}
    member_info: dict[UUID, ReducedMemberResponse] = {}
    for member_id in unique_member_ids:
        try:
            info = await member_service.get_member(access, member_id)
            if info:
                member_info[member_id] = ReducedMemberResponse.model_validate(info)
        except Exception:
            pass

    custom_info: dict[UUID, CustomResponse] = {}
    per_member_custom_ids: dict[UUID, set[UUID]] = {}
    for p in players:
        if p.custom_id:
            per_member_custom_ids.setdefault(p.member_id, set()).add(p.custom_id)
    for member_id, target_custom_ids in per_member_custom_ids.items():
        try:
            customs = await custom_service.get_customs_by_member(access, member_id)
            for c in customs:
                if c.id in target_custom_ids:
                    mapped = await remapper_service.map_customs_response([c])
                    if mapped:
                        custom_info[c.id] = mapped[0]
        except Exception:
            pass

    return await remapper_service.map_players_response(players, member_info, custom_info)


@router.patch("/{event_id}/players/{member_id}/status", response_model=PlayerUpdateResultResponse)
async def update_player_status(
    user_id: AuthorizedUserID,
    server_id: UUID,
    event_id: UUID,
    member_id: UUID,
    body: UpdatePlayerStatusRequest,
    event_service: MixerEventServiceDependency,
    member_service: MemberServiceDependency,
    custom_service: MemberCustomServiceDependency,
    remapper_service: RemapperServiceDependency,
):
    access = await get_access(server_id, user_id, member_service)
    result = await event_service.update_player_status(access, event_id, member_id, body)

    member = await member_service.get_member(access, result.member_id)
    member_info = {result.member_id: ReducedMemberResponse.model_validate(member)} if member else {}

    custom_info: dict[UUID, CustomResponse] = {}
    if result.custom_id:
        try:
            customs = await custom_service.get_customs_by_member(access, member_id)
            for c in customs:
                if c.id == result.custom_id:
                    mapped = await remapper_service.map_customs_response([c])
                    if mapped:
                        custom_info[c.id] = mapped[0]
                    break
        except Exception:
            pass

    return await remapper_service.map_player_update_result_response(
        result, member_info, custom_info
    )


@router.delete("/{event_id}/players/{member_id}", response_model=StatusResponse)
async def remove_player(
    user_id: AuthorizedUserID,
    server_id: UUID,
    event_id: UUID,
    member_id: UUID,
    event_service: MixerEventServiceDependency,
    member_service: MemberServiceDependency,
):
    access = await get_access(server_id, user_id, member_service)
    return await event_service.remove_player(access, event_id, member_id)


@router.post("/{event_id}/players", response_model=EventPlayerResponse, status_code=201)
async def add_player(
    user_id: AuthorizedUserID,
    server_id: UUID,
    event_id: UUID,
    body: AddPlayerRequest,
    event_service: MixerEventServiceDependency,
    member_service: MemberServiceDependency,
    custom_service: MemberCustomServiceDependency,
    remapper_service: RemapperServiceDependency,
):
    access = await get_access(server_id, user_id, member_service)
    result = await event_service.add_player(access, event_id, body)

    member = await member_service.get_member(access, result.member_id)
    member_info = {result.member_id: ReducedMemberResponse.model_validate(member)} if member else {}

    custom_info: dict[UUID, CustomResponse] = {}
    if result.custom_id:
        try:
            customs = await custom_service.get_customs_by_member(access, body.member_id)
            for c in customs:
                if c.id == result.custom_id:
                    mapped = await remapper_service.map_customs_response([c])
                    if mapped:
                        custom_info[c.id] = mapped[0]
                    break
        except Exception:
            pass

    mapped = await remapper_service.map_players_response([result], member_info, custom_info)
    return mapped[0]


@router.put("/{event_id}/players/{member_id}/roles", response_model=EventPlayerResponse)
async def update_player_roles(
    user_id: AuthorizedUserID,
    server_id: UUID,
    event_id: UUID,
    member_id: UUID,
    body: UpdatePlayerRolesRequest,
    event_service: MixerEventServiceDependency,
    member_service: MemberServiceDependency,
    remapper_service: RemapperServiceDependency,
):
    access = await get_access(server_id, user_id, member_service)
    result = await event_service.update_player_roles(access, event_id, member_id, body)

    member = await member_service.get_member(access, result.member_id)
    member_info = {result.member_id: ReducedMemberResponse.model_validate(member)} if member else {}

    mapped = await remapper_service.map_players_response([result], member_info)
    return mapped[0]
