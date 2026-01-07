from uuid import UUID
from fastapi import UploadFile
from fastapi_controllers import Controller, get, post, put, patch, delete

from ....dependency import (
    AuthorizedUserID,
    MemberServiceDependency,
    RatingServiceDependency,
    RemapperServiceDependency,
)
from src.domain.models.server.rating.request import (
    RatingItemCreateRequest,
    RatingItemUpdateRequest,
    RatingSetUpdateRequest,
)
from src.domain.models.server.rating.response import (
    RatingItemResponse,
    RatingSetResponse,
)
from src.domain.models.response import StatusResponse


class ServerRatingController(Controller):
    prefix = "/{server_id}/rating-set"
    tags = ["Server rating"]

    def __init__(
        self, user_id: AuthorizedUserID, remapper_service: RemapperServiceDependency
    ) -> None:
        self.user_id = user_id
        self.remapper_service = remapper_service

    @get("/", response_model=list[RatingSetResponse])
    async def get_rating_set(
        self,
        server_id: UUID,
        member_service: MemberServiceDependency,
        rating_service: RatingServiceDependency,
    ):
        access = await member_service.get_member_by_user(server_id, self.user_id)
        rating_set = await rating_service.get_rating_set(access)
        return (await self.remapper_service.map_rating_sets_response([rating_set]))[0]

    @patch("/{rating_set_id}", response_model=RatingSetResponse)
    async def update_rating_set(
        self,
        server_id: UUID,
        rating_set_id: UUID,
        body: RatingSetUpdateRequest,
        member_service: MemberServiceDependency,
        rating_service: RatingServiceDependency,
    ):
        access = await member_service.get_member_by_user(server_id, self.user_id)
        rating_set = await rating_service.update_rating_set(
            access, rating_set_id, body.name, body.min_rating, body.max_rating
        )
        return (await self.remapper_service.map_rating_sets_response([rating_set]))[0]

    @post("/{rating_set_id}/ratings", response_model=RatingItemResponse)
    async def create_rating(
        self,
        server_id: UUID,
        rating_set_id: UUID,
        body: RatingItemCreateRequest,
        member_service: MemberServiceDependency,
        rating_service: RatingServiceDependency,
    ):
        access = await member_service.get_member_by_user(server_id, self.user_id)
        rating_item = await rating_service.create_rating(
            access, rating_set_id, body.threshold, None
        )
        return (await self.remapper_service.map_rating_items_response([rating_item]))[0]

    @patch("/{rating_set_id}/ratings/{rating_id}", response_model=RatingItemResponse)
    async def update_rating(
        self,
        server_id: UUID,
        rating_set_id: UUID,
        rating_id: UUID,
        body: RatingItemUpdateRequest,
        member_service: MemberServiceDependency,
        rating_service: RatingServiceDependency,
    ):
        access = await member_service.get_member_by_user(server_id, self.user_id)
        rating_item = await rating_service.update_rating(
            access, rating_id, threshold=body.threshold
        )
        return (await self.remapper_service.map_rating_items_response([rating_item]))[0]

    @delete("/{rating_set_id}/ratings/{rating_id}", response_model=StatusResponse)
    async def delete_rating(
        self,
        server_id: UUID,
        rating_set_id: UUID,
        rating_id: UUID,
        member_service: MemberServiceDependency,
        rating_service: RatingServiceDependency,
    ):
        access = await member_service.get_member_by_user(server_id, self.user_id)
        await rating_service.delete_rating(access, rating_id)
        return StatusResponse(status="success")

    @put("/{rating_set_id}/ratings/{rating_id}/icon", response_model=RatingItemResponse)
    async def update_rating_icon(
        self,
        server_id: UUID,
        rating_set_id: UUID,
        rating_id: UUID,
        icon: UploadFile,
        member_service: MemberServiceDependency,
        rating_service: RatingServiceDependency,
    ):
        access = await member_service.get_member_by_user(server_id, self.user_id)
        # TODO : implement
        pass
