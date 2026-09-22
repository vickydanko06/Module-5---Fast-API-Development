# exercises/custom-errors/app/exceptions.py
# L7 — Custom exception classes
#
# Your task: Define custom exception classes and the handler functions
# that convert them into consistent JSON responses.

# TODO: Define three custom exception classes:
#   1. NotFoundError   — raised when a resource doesn't exist
#   2. DuplicateError  — raised when a unique constraint would be violated
#   3. ValidationError — raised for domain-level validation (beyond Pydantic)
#
# Each should store a detail message.
# Inherit from Exception.
#
# Key concept: Custom exception classes vs HTTPException
#   HTTPException is fine for simple cases, but custom exceptions let you:
#   - Raise domain errors deep in service/helper code without importing FastAPI
#   - Attach extra context (e.g., field name, resource id)
#   - Centralise error formatting in one place (the handler functions below)
#   - Write cleaner unit tests (test for the exception type, not status codes)

from fastapi import Request
from fastapi.responses import JSONResponse


class NotFoundError(Exception):
    """Raised when a requested resource does not exist."""
    def __init__(self, message: str):
        # TODO: store message on self and call super().__init__(message)
        self.detail = message
        super().__init__(message)


class DuplicateError(Exception):
    """Raised when creating a resource would violate a uniqueness constraint."""
    def __init__(self, message: str):
        self.detail = message
        super().__init__(message)


class AppValidationError(Exception):
    """Raised for domain-level validation failures (beyond Pydantic schema checks)."""
    def __init__(self, message: str):
        self.detail = message
        super().__init__(message)


# TODO: Import Request and JSONResponse so you can write handler functions
# from fastapi import Request
# from fastapi.responses import JSONResponse

# TODO: Write handler functions for each exception type.
# Each handler receives (request, exc) and returns a JSONResponse.
#
# The response body should follow this consistent format:
# {
#   "error":       "NotFoundError",     ← exception class name
#   "message":     "Student 99 not found",
#   "status_code": 404
# }
#
# Hint:
# async def not_found_handler(request: Request, exc: NotFoundError):
#     return JSONResponse(status_code=404, content={...})

async def not_found_handler(request: Request, exc: NotFoundError):
    """Handles NotFoundError → 404 response."""
    return JSONResponse(
        status_code=404,
        content={
            "error": "NotFoundError",
            "message": exc.detail,
            "status_code": 404,
        },
    )

async def duplicate_handler(request, exc: DuplicateError):
    """Handles DuplicateError → 409 response."""

    return JSONResponse(
            status_code=409,
            content={
                "error": "DuplicateError",
                "message": exc.detail,
                "status_code": 409,
            },
        )


async def app_validation_handler(request, exc: AppValidationError):
    """Handles AppValidationError → 422 response."""
    return JSONResponse(
            status_code=422,
            content={
                "error": "AppValidationError",
                "message": exc.detail,
                "status_code": 422,
            },
        )