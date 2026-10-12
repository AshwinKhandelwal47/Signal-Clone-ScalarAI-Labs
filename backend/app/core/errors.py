<<<<<<< HEAD
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class AppError(Exception):
    """Base class for expected errors. Rendered as {"error": {"code", "message"}}."""

    status_code = 400
    code = "BAD_REQUEST"

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class BadRequest(AppError):
    pass


class Unauthorized(AppError):
    status_code = 401
    code = "UNAUTHORIZED"


class Forbidden(AppError):
    status_code = 403
    code = "FORBIDDEN"


class NotFound(AppError):
    status_code = 404
    code = "NOT_FOUND"


class Conflict(AppError):
    status_code = 409
    code = "CONFLICT"


def _error_response(status_code: int, code: str, message: str) -> JSONResponse:
    return JSONResponse(
        status_code=status_code, content={"error": {"code": code, "message": message}}
    )


async def app_error_handler(_request: Request, exc: AppError) -> JSONResponse:
    return _error_response(exc.status_code, exc.code, exc.message)


async def validation_error_handler(_request: Request, exc: RequestValidationError) -> JSONResponse:
    first = exc.errors()[0] if exc.errors() else {}
    field = ".".join(str(part) for part in first.get("loc", [])[1:])
    message = first.get("msg", "Invalid request")
    return _error_response(422, "VALIDATION_ERROR", f"{field}: {message}" if field else message)
=======
"""Application error hierarchy and FastAPI exception handlers."""

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class AppError(Exception):
    """Base class for expected errors. Rendered as {"error": {"code", "message"}}."""

    status_code = 400
    code = "BAD_REQUEST"

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class BadRequest(AppError):
    """HTTP 400 Bad Request."""

    pass


class Unauthorized(AppError):
    """HTTP 401 Unauthorized: missing, expired, or invalid credentials."""

    status_code = 401
    code = "UNAUTHORIZED"


class Forbidden(AppError):
    """HTTP 403 Forbidden: authenticated caller lacks permission."""

    status_code = 403
    code = "FORBIDDEN"


class NotFound(AppError):
    """HTTP 404 Not Found: requested entity does not exist or caller cannot view it."""

    status_code = 404
    code = "NOT_FOUND"


class Conflict(AppError):
    """HTTP 409 Conflict: resource or constraint collision."""

    status_code = 409
    code = "CONFLICT"


def _error_response(status_code: int, code: str, message: str) -> JSONResponse:
    """Formats uniform JSON payload for all application errors."""
    return JSONResponse(
        status_code=status_code, content={"error": {"code": code, "message": message}}
    )


async def app_error_handler(_request: Request, exc: AppError) -> JSONResponse:
    """Catches custom AppError exceptions and translates them to HTTP JSON responses."""
    return _error_response(exc.status_code, exc.code, exc.message)


async def validation_error_handler(_request: Request, exc: RequestValidationError) -> JSONResponse:
    """Formats Pydantic request validation errors into user-friendly message strings."""
    first = exc.errors()[0] if exc.errors() else {}
    field = ".".join(str(part) for part in first.get("loc", [])[1:])
    message = first.get("msg", "Invalid request")
    return _error_response(422, "VALIDATION_ERROR", f"{field}: {message}" if field else message)

>>>>>>> 653fe1e (commented code)
