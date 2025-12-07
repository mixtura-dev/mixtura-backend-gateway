import logging
from fastapi import Request, Response
from fastapi_controllers import Controller, get, post, put

from ..exceptions import AlreadyAuthorizedException

from ...dependency import AuthServiceDependency, AuthorizedUserID

from ..models.auth.response import BusyResponse, Providers, VerifyResponse

from ..models.auth.request import (
    EmailRequest,
    EmailVerifyRequest,
    OAuthConfirm,
    PasswordConfirmRequest,
    SignInRequest,
    SignupConfirmRequest,
    UsernameRequest,
)

from ..models.response import StatusResponse, UpdateResponse

from ..models.auth.user_info import UserModel


class AuthController(Controller):
    prefix = "/auth"
    tags = ["auth"]

    def __init__(self, auth_service: AuthServiceDependency) -> None:
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.auth_service = auth_service

    @get("/user", response_model=UserModel)
    async def get_user_info(self, request: Request):
        token = request.cookies.get("token")
        user_info = await self.auth_service.get_user_info_from_auth(token)
        return user_info.model_dump()

    @put("/user", response_model=UpdateResponse)
    # TODO: do patch here instead of put
    async def update_username(
        self, request: Request, data: UsernameRequest, user_id: AuthorizedUserID
    ) -> UpdateResponse:
        result = await self.auth_service.update_username(data.username, user_id)
        return UpdateResponse(updated=result.updated)

    @post("/signin", response_model=StatusResponse)
    async def sign_in(
        self, request: Request, data: SignInRequest, response: Response
    ) -> StatusResponse:
        token = request.cookies.get("token")
        authorized = bool(await self.auth_service.get_user_from_auth_optional(token))
        if authorized:
            raise AlreadyAuthorizedException()
        token = await self.auth_service.sign_in(data.login, data.password)
        response.set_cookie("token", token.token, httponly=True, max_age=token.expires)
        return StatusResponse()

    @post("/signout", response_model=StatusResponse)
    async def sign_out(
        self, request: Request, response: Response, user_id: AuthorizedUserID
    ) -> StatusResponse:
        token = request.cookies.get("token")
        await self.auth_service.sign_out(token)
        response.delete_cookie("token")
        return StatusResponse()

    @post("/reset", response_model=StatusResponse)
    async def reset(self, data: EmailRequest) -> StatusResponse:
        await self.auth_service.reset(data.email)
        return StatusResponse()

    @post("/reset/verify", response_model=VerifyResponse)
    async def verify_reset(self, data: EmailVerifyRequest) -> VerifyResponse:
        await self.auth_service.reset_verify(data.email, data.token)
        return VerifyResponse(verified=True)

    @post("/reset/confirm", response_model=VerifyResponse)
    async def confirm_reset(
        self, request: Request, data: PasswordConfirmRequest
    ) -> VerifyResponse:
        token = request.cookies.get("token")
        authorized = bool(await self.auth_service.get_user_from_auth_optional(token))
        await self.auth_service.confirm_reset(
            data.email,
            data.token,
            data.password,
            data.repeat_password,
            token if authorized else None,
        )
        return VerifyResponse(verified=True)

    @post("/signup", response_model=StatusResponse)
    async def sign_up(self, data: EmailRequest) -> StatusResponse:
        await self.auth_service.sign_up(data.email)
        return StatusResponse()

    @post("/signup/verify", response_model=VerifyResponse)
    async def verify_sign_up(self, data: EmailVerifyRequest) -> VerifyResponse:
        await self.auth_service.sign_up_verify(data.email, data.token)
        return VerifyResponse(verified=True)

    @post("/signup/confirm", response_model=VerifyResponse)
    async def confirm_sign_up(
        self, data: SignupConfirmRequest, response: Response
    ) -> VerifyResponse:
        verified, token, expiries = await self.auth_service.sign_up_confirm(
            data.email, data.token, data.password, data.username, data.repeat_password
        )
        if token:
            response.set_cookie("token", token, httponly=True, max_age=expiries)
            return VerifyResponse(verified=True)
        return VerifyResponse(verified=verified)

    @get("/providers", response_model=Providers)
    async def providers(self):
        return await self.auth_service.get_providers()

    @post("/callback")
    async def callback(self, data: OAuthConfirm, request: Request, response: Response):
        token = request.cookies.get("token")
        user_Id = await self.auth_service.get_user_from_auth_optional(token)
        token, expires = await self.auth_service.callback(
            data.code, data.provider, user_Id
        )
        if token:
            response.set_cookie("token", token, httponly=True, max_age=expires)
        return StatusResponse()

    @post("/check", response_model=BusyResponse)
    async def check(self, data: UsernameRequest):
        result = await self.auth_service.check_username(data.username)
        return BusyResponse(busy=result.busy)
