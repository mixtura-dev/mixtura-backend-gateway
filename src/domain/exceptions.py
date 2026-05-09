from fastapi import HTTPException
from starlette.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_409_CONFLICT,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_503_SERVICE_UNAVAILABLE,
)


class NotAuthorizedException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=HTTP_401_UNAUTHORIZED,
            detail={"status": "error", "message": "Not authorized"},
        )


class AlreadyAuthorizedException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=HTTP_409_CONFLICT,
            detail={"status": "error", "message": "Already authorized"},
        )


class ServiceException(HTTPException):
    def __init__(self, status_code: int, message: str):
        super().__init__(
            status_code=status_code, detail={"status": "error", "message": message}
        )


class InternalLogicException(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"status": "error", "message": message},
        )


class RabbitTimeoutException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=HTTP_503_SERVICE_UNAVAILABLE,
            detail={"status": "error", "message": "Service is temporarily unavailable"},
        )


class RpcTimeoutError(Exception):
    """Transport-level timeout waiting for RPC reply."""


class RpcOverloadedError(Exception):
    """Transport-level error: max concurrent RPC limit reached."""


class RpcPublishError(Exception):
    """Transport-level error: failed to publish RPC request message."""


class RpcClientClosedError(Exception):
    """Transport-level error: RPC client is not running or already stopped."""
