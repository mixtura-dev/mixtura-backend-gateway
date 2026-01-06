from fastapi import APIRouter
from .auth import AuthController
from .server import router as ServerController


router = APIRouter(
    prefix="/api",
)

router.include_router(AuthController.create_router())
router.include_router(ServerController)
