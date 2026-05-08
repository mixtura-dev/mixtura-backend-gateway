from uuid import UUID
from faststream.rabbit import RabbitBroker, RabbitMessage

from src.infra.communication.rpc import rpc_request
from ..models.rating.request import (
    GetServerRatingSetsRequest,
    RatingItemCreateRequest,
    RatingItemDeleteRequest,
    RatingItemUpdateRequest,
    RatingSetUpdateRequest,
)
from ..models.request import AccessDataRequest
from ..models.rating.response import RatingItemResponse, RatingSetResponse
from ..models.response import ErrorResponse, ResponseMessage, StatusResponse
from src.domain.models.access import AccessData


class RatingRepository:
    def __init__(self, broker: RabbitBroker):
        self.broker = broker

    async def get_global_rating_templates(
        self,
    ) -> ResponseMessage[list[RatingSetResponse] | ErrorResponse]:
        response: RabbitMessage = await rpc_request(self.broker, 
            None, queue="rating_set.get_global"
        )
        return ResponseMessage[
            list[RatingSetResponse] | ErrorResponse
        ].model_validate_json(response.body)

    async def get_rating_set(
        self, access: AccessData
    ) -> ResponseMessage[RatingSetResponse | ErrorResponse]:
        request = GetServerRatingSetsRequest(
            access_data=AccessDataRequest(
                member_id=access.member_id,
                server_id=access.server_id,
                permission_mask=access.permission_mask,
                restriction_mask=access.restriction_mask,
            )
        )
        response: RabbitMessage = await rpc_request(self.broker, 
            request, queue="rating_set.get_by_server"
        )
        return ResponseMessage[RatingSetResponse | ErrorResponse].model_validate_json(
            response.body
        )

    async def update_rating_set(
        self,
        access: AccessData,
        rating_set_id: UUID,
        name: str | None = None,
        min_rating: int | None = None,
        max_rating: int | None = None,
    ) -> ResponseMessage[RatingSetResponse | ErrorResponse]:
        access_data = AccessDataRequest(
            member_id=access.member_id,
            server_id=access.server_id,
            permission_mask=access.permission_mask,
            restriction_mask=access.restriction_mask,
        )
        request = RatingSetUpdateRequest(
            access_data=access_data,
            rating_set_id=rating_set_id,
            name=name,
            min_rating=min_rating,
            max_rating=max_rating,
        )
        response: RabbitMessage = await rpc_request(self.broker, 
            request, queue="rating_set.update"
        )
        return ResponseMessage[RatingSetResponse | ErrorResponse].model_validate_json(
            response.body
        )

    async def create_rating(
        self,
        access: AccessData,
        rating_set_id: UUID,
        threshold: int,
        icon_id: UUID | None,
    ) -> ResponseMessage[RatingItemResponse | ErrorResponse]:
        access_data = AccessDataRequest(
            member_id=access.member_id,
            server_id=access.server_id,
            permission_mask=access.permission_mask,
            restriction_mask=access.restriction_mask,
        )
        request = RatingItemCreateRequest(
            access_data=access_data,
            rating_set_id=rating_set_id,
            threshold=threshold,
            icon_id=icon_id,
        )
        response: RabbitMessage = await rpc_request(self.broker, 
            request, queue="rating_set.rating.create"
        )
        return ResponseMessage[RatingItemResponse | ErrorResponse].model_validate_json(
            response.body
        )

    async def update_rating(
        self,
        access: AccessData,
        rating_item_id: UUID,
        threshold: int | None = None,
        icon_id: UUID | None = None,
    ) -> ResponseMessage[RatingItemResponse | ErrorResponse]:
        access_data = AccessDataRequest(
            member_id=access.member_id,
            server_id=access.server_id,
            permission_mask=access.permission_mask,
            restriction_mask=access.restriction_mask,
        )
        request = RatingItemUpdateRequest(
            access_data=access_data,
            rating_item_id=rating_item_id,
            threshold=threshold,
            icon_id=icon_id,
        )
        response: RabbitMessage = await rpc_request(self.broker, 
            request, queue="rating_set.rating.update"
        )
        return ResponseMessage[RatingItemResponse | ErrorResponse].model_validate_json(
            response.body
        )

    async def delete_rating(
        self,
        access: AccessData,
        rating_item_id: UUID,
    ) -> ResponseMessage[StatusResponse | ErrorResponse]:
        request = RatingItemDeleteRequest(
            access_data=AccessDataRequest(
                member_id=access.member_id,
                server_id=access.server_id,
                permission_mask=access.permission_mask,
                restriction_mask=access.restriction_mask,
            ),
            rating_item_id=rating_item_id,
        )
        response: RabbitMessage = await rpc_request(self.broker, 
            request, queue="rating_set.rating.delete"
        )
        return ResponseMessage[StatusResponse | ErrorResponse].model_validate_json(
            response.body
        )
