from uuid import UUID
from ..exceptions import ServiceException
from src.infra.communication.server.repository.rating import RatingRepository
from src.infra.communication.server.models.response import ErrorResponse
from src.domain.models.access import AccessData


class RatingService:
    def __init__(self, rating_repository: RatingRepository) -> None:
        self.rating_repository = rating_repository

    async def get_global_rating_templates(self):
        response = await self.rating_repository.get_global_rating_templates()
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message

    async def get_rating_set(self, access: AccessData):
        response = await self.rating_repository.get_rating_set(access)
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message

    async def update_rating_set(
        self,
        access: AccessData,
        rating_set_id: UUID,
        name: str | None = None,
        min_rating: int | None = None,
        max_rating: int | None = None,
    ):
        response = await self.rating_repository.update_rating_set(
            access, rating_set_id, name, min_rating, max_rating
        )
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message

    async def create_rating(
        self,
        access: AccessData,
        rating_set_id: UUID,
        threshold: int,
        icon_id: UUID | None,
    ):
        response = await self.rating_repository.create_rating(
            access, rating_set_id, threshold, icon_id
        )
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message

    async def update_rating(self, access: AccessData, rating_item_id: UUID, **kwargs):
        response = await self.rating_repository.update_rating(
            access, rating_item_id, **kwargs
        )
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message

    async def delete_rating(self, access: AccessData, rating_item_id: UUID):
        response = await self.rating_repository.delete_rating(access, rating_item_id)
        if isinstance(response.message, ErrorResponse):
            raise ServiceException(response.status, response.message.message)
        return response.message
