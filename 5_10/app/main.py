# exercises/background-tasks/app/main.py
# L9 — Background Tasks
#
# Run with: uvicorn app.main:app --reload  (from background-tasks/ folder)

from fastapi import FastAPI

# TODO: Import the reports router
from app.routers import reports

app = FastAPI(title="Background Tasks Demo")

# TODO: Include the reports router with prefix="/reports" and prefix for notifications
app.include_router(
    reports.router,
    prefix="/reports",
    tags=["reports"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)