from uuid import UUID

from faststream.rabbit import RabbitBroker, RabbitMessage

from src.infra.communication.rpc import rpc_request

from ..models.request import AccessDataRequest, PaginationRequest
from src.domain.models.access import AccessData

from ..models.core.request import (
    GetPublicServersRequest,
    GetUserServersRequest,
    ServerCreateRequest,
    ServerDeleteRequest,
    ServerGetRequest,
    ServerUpdateRequest,
)

from ..models.core.response import ServerDetailResponse, ServerListResponse

from ..models.response import ErrorResponse, ResponseMessage, StatusResponse


class ServerCoreRepository:
    def __init__(self, broker: RabbitBroker):
        self.broker = broker

    async def get_public_servers(
        self, page: int, page_size: int, name_filter: str = ""
    ) -> ResponseMessage[list[ServerListResponse] | ErrorResponse]:
        request = GetPublicServersRequest(
            pagination=PaginationRequest(page=page, page_size=page_size),
            name_filter=name_filter,
        )
        response: RabbitMessage = await rpc_request(self.broker, 
            request, queue="server.public_server_list"
        )
        return ResponseMessage[
            list[ServerListResponse] | ErrorResponse
        ].model_validate_json(response.body)

    async def get_user_servers(
        self, user_id: UUID, page: int, page_size: int, name_filter: str = ""
    ) -> ResponseMessage[list[ServerListResponse] | ErrorResponse]:
        request = GetUserServersRequest(
            user_id=user_id,
            pagination=PaginationRequest(page=page, page_size=page_size),
            name_filter=name_filter,
        )
        response: RabbitMessage = await rpc_request(self.broker, 
            request, queue="server.user_server_list"
        )
        return ResponseMessage[
            list[ServerListResponse] | ErrorResponse
        ].model_validate_json(response.body)

    async def create_server(
        self,
        user_id: UUID,
        user_name: str,
        name: str,
        public: bool,
        description: str = "",
        rating_set_id: UUID | None = None,
        role_set_id: UUID | None = None,
    ) -> ResponseMessage[ServerDetailResponse | ErrorResponse]:
        request = ServerCreateRequest(
            user_id=user_id,
            user_name=user_name,
            name=name,
            public=public,
            description=description,
            rating_set_id=rating_set_id,
            role_set_id=role_set_id,
        )
        response: RabbitMessage = await rpc_request(self.broker, 
            request, queue="server.create"
        )
        return ResponseMessage[
            ServerDetailResponse | ErrorResponse
        ].model_validate_json(response.body)

    async def get_server(
        self, access: AccessData
    ) -> ResponseMessage[ServerDetailResponse | ErrorResponse]:
        access_data = AccessDataRequest(
            member_id=access.member_id,
            server_id=access.server_id,
            permission_mask=access.permission_mask,
            restriction_mask=access.restriction_mask,
        )
        request = ServerGetRequest(access_data=access_data)
        response: RabbitMessage = await rpc_request(self.broker, 
            request, queue="server.get_info"
        )
        return ResponseMessage[
            ServerDetailResponse | ErrorResponse
        ].model_validate_json(response.body)

    async def update_server(
        self,
        access: AccessData,
        name: str | None = None,
        description: str | None = None,
        public: bool | None = None,
        banner_id: UUID | None = None,
        icon_id: UUID | None = None,
    ) -> ResponseMessage[ServerDetailResponse | ErrorResponse]:
        access_data = AccessDataRequest(
            member_id=access.member_id,
            server_id=access.server_id,
            permission_mask=access.permission_mask,
            restriction_mask=access.restriction_mask,
        )
        request = ServerUpdateRequest(
            access_data=access_data,
            name=name,
            description=description,
            public=public,
            banner_id=banner_id,
            icon_id=icon_id,
        )
        response: RabbitMessage = await rpc_request(self.broker, 
            request, queue="server.update"
        )
        return ResponseMessage[
            ServerDetailResponse | ErrorResponse
        ].model_validate_json(response.body)

    async def delete_banner(
        self, access: AccessData
    ) -> ResponseMessage[StatusResponse | ErrorResponse]:
        access_data = AccessDataRequest(
            member_id=access.member_id,
            server_id=access.server_id,
            permission_mask=access.permission_mask,
            restriction_mask=access.restriction_mask,
        )
        request = ServerDeleteRequest(access_data=access_data)
        response: RabbitMessage = await rpc_request(self.broker, 
            request, queue="server.banner.delete"
        )
        return ResponseMessage[StatusResponse | ErrorResponse].model_validate_json(
            response.body
        )

    async def delete_icon(
        self, access: AccessData
    ) -> ResponseMessage[StatusResponse | ErrorResponse]:
        access_data = AccessDataRequest(
            member_id=access.member_id,
            server_id=access.server_id,
            permission_mask=access.permission_mask,
            restriction_mask=access.restriction_mask,
        )
        request = ServerDeleteRequest(access_data=access_data)
        response: RabbitMessage = await rpc_request(self.broker, 
            request, queue="server.icon.delete"
        )
        return ResponseMessage[StatusResponse | ErrorResponse].model_validate_json(
            response.body
        )

    async def delete_server(
        self, access: AccessData
    ) -> ResponseMessage[StatusResponse | ErrorResponse]:
        access_data = AccessDataRequest(
            member_id=access.member_id,
            server_id=access.server_id,
            permission_mask=access.permission_mask,
            restriction_mask=access.restriction_mask,
        )
        request = ServerDeleteRequest(access_data=access_data)
        response: RabbitMessage = await rpc_request(self.broker, 
            request, queue="server.delete"
        )
        return ResponseMessage[StatusResponse | ErrorResponse].model_validate_json(
            response.body
        )
