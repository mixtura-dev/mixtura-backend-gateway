from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware

import src.domain.api as api
from src.env_config import env
from src.infra.redis import RedisSessionManager
from faststream.rabbit.fastapi import RabbitRouter

rabbit_router = RabbitRouter(env.rabbit.url)


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_engine = RedisSessionManager(env.redis.url)
    app.state.rabbit_router = rabbit_router
    app.state.redis_manager = redis_engine
    yield

    if await redis_engine.opened:
        await redis_engine.close()


app = FastAPI(
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    title="Mixtura",
    version="2.0",
    middleware=[Middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"])],
    lifespan=lifespan,
)

app.include_router(rabbit_router)
app.include_router(api.router)
