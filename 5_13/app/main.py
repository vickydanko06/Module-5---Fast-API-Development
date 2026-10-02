# exercises/polished-docs/app/main.py
# L12 — Polished Documentation
#
# Your task: Configure the FastAPI app with rich documentation metadata and
# include the items router with tags and descriptions.
#
# Run with: uvicorn app.main:app --reload  (from polished-docs/ folder)
# Docs at:  http://127.0.0.1:8000/docs

from fastapi import FastAPI

# TODO: Import items router
from app.routers import items

# TODO: Create the FastAPI app with:
# - title (str)
# - description (str, supports markdown)
# - version (str)
# - contact dict with name, email
# - license_info dict
#
# Key concept: These fields appear at the top of the Swagger UI page and in
# the /openapi.json schema. They help API consumers understand what your API
# does before they look at individual endpoints.
openapi_tags =[
    {
        "name": "items",
        "description": "Manage inventory items. You can list, create, and retrieve items. Filtering, sorting, and pagination features will be added in future versions.",
    }
]   
app = FastAPI(
    title="Polish your API Documentation",
    description="This API allows you to manage inventory items. You can list, create, and retrieve items. The API supports filtering, sorting, and pagination (coming soon).",
    version="1.0.0",
    contact={
        "name": "Your Name",
        "email": "vicky.@example.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },openapi_tags=openapi_tags,
)  

# TODO: Define openapi_tags — a list of tag metadata dicts
# Each dict has "name" and "description" keys
# Tags group endpoints in the Swagger sidebar
#
# Example:
# openapi_tags = [
#     {"name": "items", "description": "Manage inventory items. ..."},
# ]

# TODO: Pass openapi_tags=openapi_tags to FastAPI() constructor above


# TODO: Include the items router with prefix="/items", tags=["items"]
app.include_router(
    items.router,
    prefix="/items",
    tags=["items"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)