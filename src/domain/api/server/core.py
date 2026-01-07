from uuid import UUID
from fastapi import UploadFile
from fastapi_controllers import Controller, get, post, put, patch, delete

from ...models.server.roles.response import PermissionResponse

from ....dependency import (
    AuthServiceDependency,
    AuthorizedUserID,
    GameRoleServiceDependency,
    MemberServiceDependency,
    RatingServiceDependency,
    RemapperServiceDependency,
    ServerCoreServiceDependency,
    ServerGamesServiceDependency,
    ServerRoleServiceDependency,
)
from ...models.server.core.request import ServerCreateRequest, ServerUpdateRequest
from ...models.server.core.response import (
    ServerDetailResponse,
    ServerListResponse,
)
from ...models.server.game_roles.response import GameRoleSetResponse
from ...models.server.games.response import GameResponse
from ...models.server.member.response import RestrictionResponse
from ...models.server.rating.response import RatingSetResponse
from ...models.response import StatusResponse


class ServerCoreController(Controller):
    prefix = ""
    tags = ["Server Core"]

    def __init__(
        self, user_id: AuthorizedUserID, remapper_service: RemapperServiceDependency
    ) -> None:
        self.user_id = user_id
        self.remapper_service = remapper_service

    @get("/global/role-set", response_model=list[GameRoleSetResponse])
    async def get_global_role_templates(
        self, game_role_service: GameRoleServiceDependency
    ):
        role_templates = await game_role_service.get_global_role_templates()
        return await self.remapper_service.map_game_role_sets_response(role_templates)

    @get("/global/rating-set", response_model=list[RatingSetResponse])
    async def get_global_rating_templates(
        self, rating_service: RatingServiceDependency
    ):
        rating_templates = await rating_service.get_global_rating_templates()
        return await self.remapper_service.map_rating_sets_response(rating_templates)

    @get("/global/permissions", response_model=list[PermissionResponse])
    async def get_global_permissions(self, role_service: ServerRoleServiceDependency):
        return await role_service.get_global_permissions()

    @get("/global/restrictions", response_model=list[RestrictionResponse])
    async def get_global_restrictions(self, member_service: MemberServiceDependency):
        return await member_service.get_global_restrictions()

    @get("/global/games", response_model=list[GameResponse])
    async def get_global_games(self, game_service: ServerGamesServiceDependency):
        games = await game_service.get_global_games()
        return await self.remapper_service.map_games_response(games)

    @get("/list/public", response_model=list[ServerListResponse])
    async def list_public_servers(self, core_service: ServerCoreServiceDependency):
        servers = await core_service.get_public_servers()
        return await self.remapper_service.map_server_list_response(servers)

    @get("/list/user", response_model=list[ServerListResponse])
    async def list_user_servers(self, core_service: ServerCoreServiceDependency):
        servers = await core_service.get_user_servers(self.user_id)
        return await self.remapper_service.map_server_list_response(servers)

    @post("/", status_code=201, response_model=ServerDetailResponse)
    async def create_server(
        self,
        body: ServerCreateRequest,
        core_service: ServerCoreServiceDependency,
        auth_service: AuthServiceDependency,
    ):
        user_info = await auth_service.get_user(self.user_id)
        new_server = await core_service.create_server(
            user_id=self.user_id,
            user_name=user_info.username,
            name=body.name,
            public=body.public,
            description=body.description,
            rating_set_id=body.rating_set_id,
            role_set_id=body.role_set_id,
        )
        return (await self.remapper_service.map_server_detail_response([new_server]))[0]

    @get("/{server_id}", response_model=ServerDetailResponse)
    async def get_server(
        self,
        server_id: UUID,
        core_service: ServerCoreServiceDependency,
        member_service: MemberServiceDependency,
    ):
        access = await member_service.get_member_by_user(server_id, self.user_id)
        server = await core_service.get_server(access)
        return (await self.remapper_service.map_server_detail_response([server]))[0]

    @patch("/{server_id}", response_model=ServerDetailResponse)
    async def update_server(
        self,
        server_id: UUID,
        body: ServerUpdateRequest,
        core_service: ServerCoreServiceDependency,
        member_service: MemberServiceDependency,
    ):
        access = await member_service.get_member_by_user(server_id, self.user_id)
        server = await core_service.update_server(
            access, **body.model_dump(exclude_unset=True)
        )
        return (await self.remapper_service.map_server_detail_response([server]))[0]

    @delete("/{server_id}", response_model=StatusResponse)
    async def delete_server(
        self,
        server_id: UUID,
        core_service: ServerCoreServiceDependency,
        member_service: MemberServiceDependency,
    ):
        access = await member_service.get_member_by_user(server_id, self.user_id)
        await core_service.delete_server(access)
        return StatusResponse()

    @put("/{server_id}/banner", response_model=ServerDetailResponse)
    async def update_banner(self, server_id: UUID, banner: UploadFile):
        # TODO : Implement
        pass

    @delete("/{server_id}/banner", response_model=StatusResponse)
    async def delete_banner(
        self,
        server_id: UUID,
        core_service: ServerCoreServiceDependency,
        member_service: MemberServiceDependency,
    ):
        access = await member_service.get_member_by_user(server_id, self.user_id)
        await core_service.delete_banner(access)
        return StatusResponse()

    @put("/{server_id}/icon", response_model=ServerDetailResponse)
    async def update_icon(self, server_id: UUID, icon: UploadFile):
        # TODO : Implement
        pass

    @delete("/{server_id}/icon", response_model=StatusResponse)
    async def delete_icon(
        self,
        server_id: UUID,
        core_service: ServerCoreServiceDependency,
        member_service: MemberServiceDependency,
    ):
        access = await member_service.get_member_by_user(server_id, self.user_id)
        await core_service.delete_icon(access)
        return StatusResponse()
