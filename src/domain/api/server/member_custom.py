from uuid import UUID
from fastapi_controllers import Controller, get, post, put, delete

from ....dependency import (
    AuthorizedUserID,
    MemberCustomServiceDependency,
    MemberServiceDependency,
    RemapperServiceDependency,
)
from src.domain.models.server.custom.request import GameRoleRatingSetRequest
from src.domain.models.server.custom.response import CustomResponse
from src.domain.models.response import StatusResponse


class MemberCustomController(Controller):
    prefix = "/{server_id}/members/{member_id}/customs"
    tags = ["Member custom"]

    def __init__(
        self, user_id: AuthorizedUserID, remapper_service: RemapperServiceDependency
    ) -> None:
        self.user_id = user_id
        self.remapper_service = remapper_service

    @get("/", response_model=list[CustomResponse])
    async def list_customs(
        self,
        server_id: UUID,
        member_id: UUID,
        member_service: MemberServiceDependency,
        custom_service: MemberCustomServiceDependency,
    ):
        access = await member_service.get_member_by_user(server_id, self.user_id)
        customs = await custom_service.get_customs_by_member(access, member_id)
        return await self.remapper_service.map_customs_response(customs)

    @post("/", response_model=CustomResponse)
    async def create_custom(
        self,
        server_id: UUID,
        member_id: UUID,
        member_service: MemberServiceDependency,
        custom_service: MemberCustomServiceDependency,
    ):
        access = await member_service.get_member_by_user(server_id, self.user_id)
        custom = await custom_service.create_custom(access, member_id)
        return (await self.remapper_service.map_customs_response([custom]))[0]

    @delete("/{custom_id}", response_model=StatusResponse)
    async def delete_custom(
        self,
        server_id: UUID,
        member_id: UUID,
        custom_id: UUID,
        member_service: MemberServiceDependency,
        custom_service: MemberCustomServiceDependency,
    ):
        access = await member_service.get_member_by_user(server_id, self.user_id)
        await custom_service.delete_custom(access, custom_id)
        return StatusResponse()

    @put("/{custom_id}/ratings/{game_role_id}", response_model=CustomResponse)
    async def update_rating_value(
        self,
        server_id: UUID,
        member_id: UUID,
        custom_id: UUID,
        game_role_id: UUID,
        body: GameRoleRatingSetRequest,
        member_service: MemberServiceDependency,
        custom_service: MemberCustomServiceDependency,
    ):
        access = await member_service.get_member_by_user(server_id, self.user_id)
        custom = await custom_service.update_custom(
            access, custom_id, game_role_id, body.rating
        )
        return (await self.remapper_service.map_customs_response([custom]))[0]
