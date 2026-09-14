# exercises/structured-recipe-api/app/main.py
# L2 — Structured Recipe API
#
# Your task: Wire the FastAPI app to the recipes router.
#
# Run with: uvicorn app.main:app --reload  (from the structured-recipe-api/ folder)
# Docs at:  http://127.0.0.1:8000/docs

# TODO: Import FastAPI
from fastapi import FastAPI
from app.routers import recipes

# TODO: Import the recipes router from app.routers.recipes
# Hint: from app.routers import recipes  OR  from app.routers.recipes import router

# Key concept: APIRouter lets you group related endpoints in a separate file,
# then "include" them in the main app with a prefix. This keeps main.py clean
# as your API grows.

# TODO: Create the FastAPI app instance
app = FastAPI()

# TODO: Include the recipes router with prefix="/recipes" and tags=["recipes"]
# Hint: app.include_router(...)

app.include_router(
    recipes.router,
    prefix="/recipes",
    tags=["recipes"]
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)