from uuid import UUID

from src.infra.communication.rabbit import RabbitRpcClient
from src.infra.communication.rpc import rpc_request
from ..models.custom.request import (
    CreateCustomRequest,
    DeleteCustomRequest,
    GetCustomsRequest,
    UpdateGameRoleRatingRequest,
)
from ..models.custom.response import CustomResponse
from ..models.response import ErrorResponse, ResponseMessage, StatusResponse
from ..models.request import AccessDataRequest
from src.domain.models.access import AccessData


class MemberCustomRepository:
    def __init__(self, rpc_client: RabbitRpcClient):
        self.rpc_client = rpc_client

    async def get_customs_by_member(
        self, access: AccessData, target_member_id: UUID
    ) -> ResponseMessage[list[CustomResponse] | ErrorResponse]:
        request = GetCustomsRequest(
            access_data=AccessDataRequest(
                member_id=access.member_id,
                server_id=access.server_id,
                permission_mask=access.permission_mask,
                restriction_mask=access.restriction_mask,
            ),
            target_member_id=target_member_id,
        )
        response = await rpc_request(self.rpc_client,
            request, queue="custom.get_by_member"
        )
        return ResponseMessage[
            list[CustomResponse] | ErrorResponse
        ].model_validate_json(response.body)

    async def create_custom(
        self, access: AccessData, target_member_id: UUID
    ) -> ResponseMessage[CustomResponse | ErrorResponse]:
        request = CreateCustomRequest(
            access_data=AccessDataRequest(
                member_id=access.member_id,
                server_id=access.server_id,
                permission_mask=access.permission_mask,
                restriction_mask=access.restriction_mask,
            ),
            target_member_id=target_member_id,
        )
        response = await rpc_request(self.rpc_client,
            request, queue="custom.create"
        )
        return ResponseMessage[CustomResponse | ErrorResponse].model_validate_json(
            response.body
        )

    async def delete_custom(
        self, access: AccessData, custom_id: UUID
    ) -> ResponseMessage[StatusResponse | ErrorResponse]:
        request = DeleteCustomRequest(
            access_data=AccessDataRequest(
                member_id=access.member_id,
                server_id=access.server_id,
                permission_mask=access.permission_mask,
                restriction_mask=access.restriction_mask,
            ),
            custom_id=custom_id,
        )
        response = await rpc_request(self.rpc_client,
            request, queue="custom.delete"
        )
        return ResponseMessage[StatusResponse | ErrorResponse].model_validate_json(
            response.body
        )

    async def update_custom(
        self,
        access: AccessData,
        custom_id: UUID,
        game_role_id: UUID,
        rating: int,
    ) -> ResponseMessage[CustomResponse | ErrorResponse]:
        request = UpdateGameRoleRatingRequest(
            access_data=AccessDataRequest(
                member_id=access.member_id,
                server_id=access.server_id,
                permission_mask=access.permission_mask,
                restriction_mask=access.restriction_mask,
            ),
            custom_id=custom_id,
            game_role_id=game_role_id,
            rating=rating,
        )
        response = await rpc_request(self.rpc_client,
            request, queue="custom.rating.set"
        )
        return ResponseMessage[CustomResponse | ErrorResponse].model_validate_json(
            response.body
        )
