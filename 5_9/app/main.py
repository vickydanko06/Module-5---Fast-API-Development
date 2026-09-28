# exercises/auth-system/app/main.py
# L8 — Auth System
#
# Run with: uvicorn app.main:app --reload  (from auth-system/ folder)

from fastapi import FastAPI
from app.database import Base, engine

# TODO: Import the auth router
from app.routers import auth

app = FastAPI(title="Auth System API")

Base.metadata.create_all(bind=engine)

# TODO: Include the auth router with prefix="/auth" and tags=["auth"]
app.include_router(
    auth.router,
    prefix="/auth",
    tags=["auth"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)