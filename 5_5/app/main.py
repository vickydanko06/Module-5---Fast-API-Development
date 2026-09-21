# exercises/database-notes/app/main.py
# L5 — Database-Backed Notes API
#
# Run with: uvicorn app.main:app --reload  (from database-notes/ folder)

from fastapi import FastAPI
from app.database import Base, engine
from app.routers import notes

app = FastAPI(title="Notes API")

# TODO: Create all database tables on startup
# Hint: Base.metadata.create_all(bind=engine)
Base.metadata.create_all(bind=engine)

# TODO: Include the notes router
# Hint: app.include_router(notes.router, prefix="/notes", tags=["notes"])
app.include_router(notes.router,prefix="/notes", tags=["notes"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)