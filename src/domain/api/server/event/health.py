from fastapi import APIRouter

from src.dependency import MixerEventServiceDependency
from src.domain.models.response import StatusResponse

router = APIRouter(tags=["Event Health"])


@router.get("/health", response_model=StatusResponse)
async def event_health(event_service: MixerEventServiceDependency):
    return await event_service.health()
