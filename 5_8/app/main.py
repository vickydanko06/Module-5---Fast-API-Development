# exercises/custom-errors/app/main.py
# L7 — Custom Error Handling
#
# Run with: uvicorn app.main:app --reload  (from custom-errors/ folder)
from fastapi import FastAPI
from app.database import Base, engine

from app.exceptions import (
    NotFoundError,
    DuplicateError,
    AppValidationError,
    not_found_handler,
    duplicate_handler,
    app_validation_handler,
)

from app.routers import students


app = FastAPI(title="Custom Errors API")

Base.metadata.create_all(bind=engine)


# Register custom exception handlers
app.add_exception_handler(NotFoundError, not_found_handler)
app.add_exception_handler(DuplicateError, duplicate_handler)
app.add_exception_handler(AppValidationError, app_validation_handler)


# Include student routes
app.include_router(students.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)