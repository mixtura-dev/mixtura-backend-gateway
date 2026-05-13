from uuid import UUID
from ..exceptions import ServiceException
from src.infra.communication.auth.repository import AuthRepository
from ...infra.communication.auth.schemas.response import ErrorResponse, TokenResponse


class AuthService:
    def __init__(self, auth_repository: AuthRepository) -> None:
        self.auth_repository = auth_repository

    async def get_user_from_auth_optional(self, token: str | None) -> UUID | None:
        if token is None:
            return None
        response = await self.auth_repository.auth_check(token)
        if isinstance(response.message, ErrorResponse):
            return None
        return response.message.user_id

    async def get_user_from_auth(self, token: str | None) -> UUID:
        if token is None:
            raise ServiceException(401, "Unauthorized")
        response = await self.auth_repository.auth_check(token)
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message.user_id
    
    async def get_user_info_from_auth(self, token: str | None):
        if token is None:
            raise ServiceException(401, "Unauthorized")
        response = await self.auth_repository.get_user_info(token)
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message
    
    async def get_user(self, user_id: UUID):
        response = await self.auth_repository.get_user(user_id)
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message

    async def get_users_bulk(self, user_ids: list[UUID]):
        response = await self.auth_repository.get_users_bulk(user_ids)
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message

    async def get_integration_accounts(self, integration_ids: list[UUID]):
        response = await self.auth_repository.get_integration_accounts(integration_ids)
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message

    async def sign_in(self, login: str, password: str):
        response = await self.auth_repository.sign_in(login, password)
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message
    
    async def sign_out(self, token: str | None):
        if token is None:
            raise ServiceException(401, "Unauthorized")
        response = await self.auth_repository.sign_out(token)
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message
    
    async def update_username(self, username: str, user_id: UUID):
        response = await self.auth_repository.update_username(username, user_id)
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message
    
    async def check_username(self, username: str):
        response = await self.auth_repository.check_username(username)
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message
    
    async def reset(self, email: str):
        response = await self.auth_repository.reset(email)
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message
    
    async def reset_verify(self, email: str, token: str):
        response = await self.auth_repository.reset_verify(email, token)
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message
    
    async def confirm_reset(self, email: str, token: str, password: str, repeat_password: str, auth_token: str | None):
        response = await self.auth_repository.reset_confirm(email, token, password, repeat_password, auth_token)
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message
    
    async def sign_up(self, email: str):
        response = await self.auth_repository.sign_up(email)
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message
    
    async def sign_up_verify(self, email: str, token: str):
        response = await self.auth_repository.sign_up_verify(email, token)
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message
    
    async def sign_up_confirm(self, email: str, token: str, password: str, username: str, repeat_password: str):
        response = await self.auth_repository.sign_up_confirm(email, token, password, username, repeat_password)
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        if isinstance(response.message, TokenResponse):
            return (True, response.message.token, response.message.expires)
        return (response.message.verified, "", 0)
    
    async def get_providers(self):
        response = await self.auth_repository.providers()
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message
    
    async def callback(self, code: str, provider: str, user_Id: UUID | None):
        response = await self.auth_repository.proccess_callback(provider, code, user_Id)
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        if isinstance(response.message, TokenResponse):
            return (response.message.token, response.message.expires)
        return ("", 0)

    async def get_user_providers(self, user_id: UUID) -> list[dict]:
        response = await self.auth_repository.get_user(user_id)
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return [
            {
                "id": p.id,
                "name": p.name,
                "client_id": p.client_id,
                "client_username": p.client_username,
            }
            for p in response.message.providers
        ]
