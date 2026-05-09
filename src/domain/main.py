from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware import Middleware

import src.domain.api as api
from src.env_config import env
from src.infra.redis import RedisSessionManager
from src.infra.communication.rabbit import RabbitRpcClient
from src.domain.exceptions import (
    RpcClientClosedError,
    RpcOverloadedError,
    RpcPublishError,
    RpcTimeoutError,
)

from faststream.rabbit.fastapi import RabbitRouter

rabbit_router = RabbitRouter(env.rabbit.url)


def _rpc_error_response(status_code: int, message: str) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={"status": "error", "message": message},
    )


async def rpc_timeout_handler(request: Request, exc: RpcTimeoutError) -> JSONResponse:
    return _rpc_error_response(504, "Upstream service timed out")


async def rpc_overloaded_handler(request: Request, exc: RpcOverloadedError) -> JSONResponse:
    return _rpc_error_response(503, "Service temporarily overloaded")


async def rpc_publish_handler(request: Request, exc: RpcPublishError) -> JSONResponse:
    return _rpc_error_response(502, "Failed to communicate with upstream service")


async def rpc_closed_handler(request: Request, exc: RpcClientClosedError) -> JSONResponse:
    return _rpc_error_response(503, "Service is not available")


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_engine = RedisSessionManager(env.redis.url)
    app.state.rabbit_router = rabbit_router
    app.state.redis_manager = redis_engine

    rpc_client = RabbitRpcClient(
        amqp_url=env.rabbit.url,
        default_timeout=env.rabbit.request_timeout,
    )
    await rpc_client.start()
    app.state.rpc_client = rpc_client

    yield

    await rpc_client.stop()

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

app.add_exception_handler(RpcTimeoutError, rpc_timeout_handler)
app.add_exception_handler(RpcOverloadedError, rpc_overloaded_handler)
app.add_exception_handler(RpcPublishError, rpc_publish_handler)
app.add_exception_handler(RpcClientClosedError, rpc_closed_handler)

app.include_router(rabbit_router)
app.include_router(api.router)
