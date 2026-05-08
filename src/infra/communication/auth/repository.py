from uuid import UUID
from faststream.rabbit import RabbitBroker, RabbitMessage

from src.infra.communication.rpc import rpc_request

from .schemas.response import (
    BusyResponse,
    ErrorResponse,
    ProvidersResponse,
    ResponseMessage,
    StatusResponse,
    TokenResponse,
    UpdateResponse,
    VerifyResponse,
)

from .schemas.user_info import AuthCheckResponse, UserResponse

from .schemas.request import (
    EmailRequest,
    EmailVerifyRequest,
    OAuthConfirmRequest,
    PasswordConfirmRequest,
    SignInRequest,
    SignupConfirmRequest,
    TokenRequest,
    UserBulkRequest,
    UserRequest,
    UsernameRequest,
    UsernameUpdateRequest,
)


class AuthRepository:
    def __init__(self, broker: RabbitBroker):
        self.broker = broker

    async def providers(self) -> ResponseMessage[ProvidersResponse | ErrorResponse]:
        request = None
        response: RabbitMessage = await rpc_request(self.broker, 
            request, queue="auth.providers"
        )
        return ResponseMessage[ProvidersResponse | ErrorResponse].model_validate_json(
            response.body
        )

    async def auth_check(
        self, token: str
    ) -> ResponseMessage[AuthCheckResponse | ErrorResponse]:
        request = TokenRequest(token=token)
        response: RabbitMessage = await rpc_request(self.broker, 
            request, queue="auth.get_auth_check"
        )
        return ResponseMessage[AuthCheckResponse | ErrorResponse].model_validate_json(
            response.body
        )

    async def get_user_info(
        self, token: str
    ) -> ResponseMessage[UserResponse | ErrorResponse]:
        request = TokenRequest(token=token)
        response: RabbitMessage = await rpc_request(self.broker, 
            request, queue="auth.get_user_info"
        )
        return ResponseMessage[UserResponse | ErrorResponse].model_validate_json(
            response.body
        )

    async def get_user(
        self, user_id: UUID
    ) -> ResponseMessage[UserResponse | ErrorResponse]:
        request = UserRequest(user_id=user_id)
        response: RabbitMessage = await rpc_request(self.broker, 
            request, queue="auth.get_user"
        )
        return ResponseMessage[UserResponse | ErrorResponse].model_validate_json(
            response.body
        )
    
    async def get_users_bulk(
        self, user_ids: list[UUID]
    ) -> ResponseMessage[dict[UUID, UserResponse] | ErrorResponse]:
        request = UserBulkRequest(user_ids=user_ids)
        response: RabbitMessage = await rpc_request(self.broker, 
            request, queue="auth.get_users.bulk"
        )
        return ResponseMessage[dict[UUID, UserResponse] | ErrorResponse].model_validate_json(
            response.body
        )

    async def sign_in(
        self, login: str, password: str
    ) -> ResponseMessage[TokenResponse | ErrorResponse]:
        request = SignInRequest(login=login, password=password)
        response: RabbitMessage = await rpc_request(self.broker, 
            request, queue="auth.signin"
        )
        return ResponseMessage[TokenResponse | ErrorResponse].model_validate_json(
            response.body
        )

    async def update_username(
        self, username: str, user_id: UUID
    ) -> ResponseMessage[UpdateResponse | ErrorResponse]:
        request = UsernameUpdateRequest(username=username, user_id=user_id)
        response: RabbitMessage = await rpc_request(self.broker, 
            request, queue="auth.update_username"
        )
        return ResponseMessage[UpdateResponse | ErrorResponse].model_validate_json(
            response.body
        )

    async def sign_out(
        self, token: str
    ) -> ResponseMessage[StatusResponse | ErrorResponse]:
        request = TokenRequest(token=token)
        response: RabbitMessage = await rpc_request(self.broker, 
            request, queue="auth.signout"
        )
        return ResponseMessage[StatusResponse | ErrorResponse].model_validate_json(
            response.body
        )

    async def sign_up(
        self, email: str
    ) -> ResponseMessage[StatusResponse | ErrorResponse]:
        request = EmailRequest(email=email)
        response: RabbitMessage = await rpc_request(self.broker, 
            request, queue="auth.signup"
        )
        return ResponseMessage[StatusResponse | ErrorResponse].model_validate_json(
            response.body
        )

    async def sign_up_verify(
        self, email: str, token: str
    ) -> ResponseMessage[StatusResponse | ErrorResponse]:
        request = EmailVerifyRequest(email=email, token=token)
        response: RabbitMessage = await rpc_request(self.broker, 
            request, queue="auth.signup.verify"
        )
        return ResponseMessage[StatusResponse | ErrorResponse].model_validate_json(
            response.body
        )

    async def sign_up_confirm(
        self, email: str, token: str, password: str, username: str, repeat_password: str
    ) -> ResponseMessage[TokenResponse | VerifyResponse | ErrorResponse]:
        request = SignupConfirmRequest(
            email=email,
            token=token,
            password=password,
            username=username,
            repeat_password=repeat_password,
        )
        response: RabbitMessage = await rpc_request(self.broker, 
            request, queue="auth.signup.confirm"
        )
        return ResponseMessage[
            TokenResponse | VerifyResponse | ErrorResponse
        ].model_validate_json(response.body)

    async def reset(
        self, email: str
    ) -> ResponseMessage[StatusResponse | ErrorResponse]:
        request = EmailRequest(email=email)
        response: RabbitMessage = await rpc_request(self.broker, request, queue="auth.reset")
        return ResponseMessage[StatusResponse | ErrorResponse].model_validate_json(
            response.body
        )

    async def reset_verify(
        self, email: str, token: str
    ) -> ResponseMessage[StatusResponse | ErrorResponse]:
        request = EmailVerifyRequest(email=email, token=token)
        response: RabbitMessage = await rpc_request(self.broker, 
            request, queue="auth.reset.verify"
        )
        return ResponseMessage[StatusResponse | ErrorResponse].model_validate_json(
            response.body
        )

    async def reset_confirm(
        self,
        email: str,
        token: str,
        password: str,
        repeat_password: str,
        auth_token: str | None,
    ) -> ResponseMessage[StatusResponse | ErrorResponse]:
        request = PasswordConfirmRequest(
            email=email,
            token=token,
            password=password,
            repeat_password=repeat_password,
            auth_token=auth_token,
        )
        response: RabbitMessage = await rpc_request(self.broker, 
            request, queue="auth.reset.confirm"
        )
        return ResponseMessage[StatusResponse | ErrorResponse].model_validate_json(
            response.body
        )

    async def check_username(
        self, username: str
    ) -> ResponseMessage[BusyResponse | ErrorResponse]:
        request = UsernameRequest(username=username)
        response: RabbitMessage = await rpc_request(self.broker, 
            request, queue="auth.check_username"
        )
        return ResponseMessage[BusyResponse | ErrorResponse].model_validate_json(
            response.body
        )

    async def proccess_callback(
        self, provider: str, code: str, user_id: UUID | None
    ) -> ResponseMessage[StatusResponse | TokenResponse | ErrorResponse]:
        request = OAuthConfirmRequest(provider=provider, code=code, user_id=user_id)
        response: RabbitMessage = await rpc_request(self.broker, 
            request, queue="auth.callback"
        )
        return ResponseMessage[
            StatusResponse | TokenResponse | ErrorResponse
        ].model_validate_json(response.body)
