from uuid import UUID
from faststream.rabbit import RabbitBroker, RabbitMessage
from ..schemas.custom.request import (
    CreateCustomRequest,
    DeleteCustomRequest,
    GetCustomsRequest,
    UpdateGameRoleRatingRequest,
)
from ..schemas.custom.response import CustomResponse
from ..schemas.response import ErrorResponse, ResponseMessage, StatusResponse
from ..schemas.request import AccessDataRequest


class CustomRepository:
    def __init__(self, broker: RabbitBroker):
        self.broker = broker

    async def get_customs_by_member(
        self, access_data: AccessDataRequest, target_member_id: UUID
    ) -> ResponseMessage[list[CustomResponse] | ErrorResponse]:
        request = GetCustomsRequest(
            access_data=access_data, target_member_id=target_member_id
        )
        response: RabbitMessage = await self.broker.request(
            request, queue="custom.get_by_member"
        )
        return ResponseMessage[
            list[CustomResponse] | ErrorResponse
        ].model_validate_json(response.body)

    async def create_custom(
        self, access_data: AccessDataRequest, target_member_id: UUID
    ) -> ResponseMessage[CustomResponse | ErrorResponse]:
        request = CreateCustomRequest(
            access_data=access_data, target_member_id=target_member_id
        )
        response: RabbitMessage = await self.broker.request(
            request, queue="custom.create"
        )
        return ResponseMessage[CustomResponse | ErrorResponse].model_validate_json(
            response.body
        )

    async def delete_custom(
        self, access_data: AccessDataRequest, custom_id: UUID
    ) -> ResponseMessage[StatusResponse | ErrorResponse]:
        request = DeleteCustomRequest(access_data=access_data, custom_id=custom_id)
        response: RabbitMessage = await self.broker.request(
            request, queue="custom.delete"
        )
        return ResponseMessage[StatusResponse | ErrorResponse].model_validate_json(
            response.body
        )

    async def update_custom(
        self,
        access_data: AccessDataRequest,
        custom_id: UUID,
        game_role_id: UUID,
        rating: int,
    ) -> ResponseMessage[CustomResponse | ErrorResponse]:
        request = UpdateGameRoleRatingRequest(
            access_data=access_data,
            custom_id=custom_id,
            game_role_id=game_role_id,
            rating=rating,
        )
        response: RabbitMessage = await self.broker.request(
            request, queue="custom.rating.set"
        )
        return ResponseMessage[CustomResponse | ErrorResponse].model_validate_json(
            response.body
        )
