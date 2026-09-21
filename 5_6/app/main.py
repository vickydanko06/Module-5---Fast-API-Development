# exercises/student-crud/app/main.py
# L6 — Student CRUD API
#
# Run with: uvicorn app.main:app --reload  (from student-crud/ folder)

from fastapi import FastAPI
from app.database import Base, engine
from app.routers.students import router as students_router

# TODO: Import the students router and include it

app = FastAPI(title="Student CRUD API")

app.include_router(
    students_router,
    prefix="/students",
    tags=["students"],
)

# TODO: Create tables
# Base.metadata.create_all(bind=engine)

Base.metadata.create_all(bind=engine)

# TODO: Include the students router

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)