from uuid import UUID
from fastapi import UploadFile
from fastapi_controllers import Controller, get, post, put, patch, delete

from ....dependency import (
    AuthorizedUserID,
    GameRoleServiceDependency,
    MemberServiceDependency,
    RemapperServiceDependency,
)
from src.domain.models.server.game_roles.request import (
    GameRoleItemCreateRequest,
    GameRoleItemUpdateRequest,
    GameRoleSetUpdateRequest,
)
from src.domain.models.server.game_roles.response import (
    GameRoleItemResponse,
    GameRoleSetResponse,
)
from src.domain.models.response import StatusResponse


class ServerGameRoleController(Controller):
    prefix = "/{server_id}/role-set"
    tags = ["Server game role"]

    def __init__(
        self, user_id: AuthorizedUserID, remapper_service: RemapperServiceDependency
    ) -> None:
        self.user_id = user_id
        self.remapper_service = remapper_service

    @get("/", response_model=GameRoleSetResponse)
    async def get_role_set(
        self,
        server_id: UUID,
        game_role_service: GameRoleServiceDependency,
        member_service: MemberServiceDependency,
    ):
        access = await member_service.get_member_by_user(server_id, self.user_id)
        game_role_set = await game_role_service.get_role_set(access)
        return (
            await self.remapper_service.map_game_role_sets_response([game_role_set])
        )[0]

    @patch("/{role_set_id}", response_model=GameRoleSetResponse)
    async def update_role_set(
        self,
        server_id: UUID,
        role_set_id: UUID,
        body: GameRoleSetUpdateRequest,
        game_role_service: GameRoleServiceDependency,
        member_service: MemberServiceDependency,
    ):
        access = await member_service.get_member_by_user(server_id, self.user_id)
        game_role_set = await game_role_service.update_role_set(
            access, role_set_id, body.name
        )
        return (
            await self.remapper_service.map_game_role_sets_response([game_role_set])
        )[0]

    @post("/{role_set_id}/role", response_model=GameRoleItemResponse)
    async def create_role(
        self,
        server_id: UUID,
        role_set_id: UUID,
        body: GameRoleItemCreateRequest,
        game_role_service: GameRoleServiceDependency,
        member_service: MemberServiceDependency,
    ):
        access = await member_service.get_member_by_user(server_id, self.user_id)
        game_role = await game_role_service.create_role(
            access=access,
            role_set_id=role_set_id,
            name=body.name,
            min_in_team=body.min_in_team,
            max_in_team=body.max_in_team,
            hidden=body.hidden,
        )
        return (await self.remapper_service.map_game_roles_response([game_role]))[0]

    @patch("/{role_set_id}/role/{role_id}", response_model=GameRoleItemResponse)
    async def update_role(
        self,
        server_id: UUID,
        role_set_id: UUID,
        role_id: UUID,
        body: GameRoleItemUpdateRequest,
        game_role_service: GameRoleServiceDependency,
        member_service: MemberServiceDependency,
    ):
        access = await member_service.get_member_by_user(server_id, self.user_id)
        new_game_role = await game_role_service.update_role(
            access=access,
            role_id=role_id,
            name=body.name,
            min_in_team=body.min_in_team,
            max_in_team=body.max_in_team,
            hidden=body.hidden,
        )
        return (await self.remapper_service.map_game_roles_response([new_game_role]))[0]

    @delete("/{role_set_id}/roles/{role_id}", response_model=StatusResponse)
    async def delete_role(
        self,
        server_id: UUID,
        role_set_id: UUID,
        role_id: UUID,
        game_role_service: GameRoleServiceDependency,
        member_service: MemberServiceDependency,
    ):
        access = await member_service.get_member_by_user(server_id, self.user_id)
        await game_role_service.delete_role(access, role_id)
        return StatusResponse()

    @put("/{role_set_id}/roles/{role_id}/icon", response_model=GameRoleItemResponse)
    async def update_role_icon(
        self, server_id: UUID, role_id: UUID, role_set_id: UUID, icon: UploadFile
    ):
        # TODO : Implement
        pass

    @delete("/{role_set_id}/roles/{role_id}/icon", response_model=StatusResponse)
    async def delete_role_icon(
        self,
        server_id: UUID,
        role_set_id: UUID,
        role_id: UUID,
        game_role_service: GameRoleServiceDependency,
        member_service: MemberServiceDependency,
    ):
        access = await member_service.get_member_by_user(server_id, self.user_id)
        await game_role_service.delete_role_icon(access, role_id)
        return StatusResponse()
