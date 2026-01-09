from fastapi import APIRouter

from .member_custom import MemberCustomController
from .member import member_router
from .core import ServerCoreController
from .game_role import ServerGameRoleController
from .game import ServerGameController
from .invite import ServerInviteController
from .rating import ServerRatingController
from .role import ServerRoleController

router = APIRouter(
    prefix="/server",
)

router.include_router(ServerCoreController.create_router())
router.include_router(ServerInviteController.create_router())
router.include_router(ServerGameController.create_router())
router.include_router(ServerGameRoleController.create_router())
router.include_router(ServerRatingController.create_router())
router.include_router(MemberCustomController.create_router())
router.include_router(member_router)
router.include_router(ServerRoleController.create_router())