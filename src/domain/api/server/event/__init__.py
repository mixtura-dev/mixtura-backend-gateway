from fastapi import APIRouter

from . import application, core, draft, health, match, organizer, player, team, team_formation

event_health_router = APIRouter(prefix="/events")
event_router = APIRouter(prefix="/{server_id}/events")

event_health_router.include_router(health.router)

event_router.include_router(core.router)
event_router.include_router(organizer.router)
event_router.include_router(application.router)
event_router.include_router(player.router)
event_router.include_router(draft.router)
event_router.include_router(team_formation.router)
event_router.include_router(team.router)
event_router.include_router(match.router)

__all__ = ["event_health_router", "event_router"]
