# exercises/structured-recipe-api/app/routers/recipes.py
# L2 — Recipe endpoints
#
# Your task: Implement the recipe CRUD endpoints using an in-memory list.

# TODO: Import APIRouter and HTTPException from fastapi
from fastapi import APIRouter, HTTPException

# TODO: Import Optional from typing (for the POST body)
from typing import Optional

# TODO: Create the router instance
# Hint: router = APIRouter()
router = APIRouter()

# In-memory "database" — a simple list of dicts.
# No real database needed for this exercise.
recipes: list[dict] = [
    {"id": 1, "title": "Pasta Carbonara", "cuisine": "Italian", "servings": 2},
    {"id": 2, "title": "Tacos al Pastor", "cuisine": "Mexican", "servings": 4},
]

# Simple counter to generate new IDs
_next_id = 3


# TODO: Implement GET / — returns the full list of recipes
# Hint: @router.get("/")
@router.get("/")
def list_recipes():
    """
    Returns all recipes.

    TODO: Return the recipes list.
    """
    pass  # TODO: implement
    return recipes


# TODO: Implement GET /{recipe_id} — returns a single recipe by id
# Return 404 if not found
@router.get("/{recipe_id}")
def get_recipe(recipe_id: int):
    for recipe in recipes:
        if(recipe["id"]== recipe_id):
            return recipe
    raise HTTPException(status_code = 404, detail="Recipe not found")
    """
    Returns a single recipe by ID.

    Args:
        recipe_id: The integer ID in the URL path.

    TODO: Search the recipes list, raise HTTPException(404) if missing.
    """
    pass  # TODO: implement


# TODO: Implement POST / — creates a new recipe
# Accept a request body dict with at least "title", "cuisine", "servings"
# Use the Body(...) import or just a Pydantic model (either is fine for now)
# Return the created recipe with its new id and HTTP 201
@router.post("/",status_code=201)
def create_recipe(recipe: dict):
    """
    Creates a new recipe and returns it with an assigned id.

    TODO:
    1. Generate a new ID (use the _next_id counter — remember to update it with global).
    2. Build the new recipe dict.
    3. Append to recipes list.
    4. Return the new recipe with status_code=201.
    """
    pass  # TODO: implement
    global _next_id
    new_recipe = {"id": _next_id, **recipe}
    recipes.append(new_recipe)
    _next_id += 1
    return new_recipe
