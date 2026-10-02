# exercises/polished-docs/app/routers/items.py
# L12 — Documented item endpoints

from fastapi import APIRouter, HTTPException
from app.schemas.item import ItemCreate, ItemResponse

router = APIRouter()

items: list[dict] = []
_next_id = 1


# TODO: Implement GET / with:
# - A detailed docstring (shown in Swagger as the endpoint description)
# - response_model=list[ItemResponse]
# - tags already applied from main.py include_router
#
# Key concept: FastAPI uses the function docstring as the endpoint description
# in the Swagger UI. Markdown is supported — use ** for bold, ` for code, etc.
@router.get(
    "/",
    response_model=list[ItemResponse],
    summary="List all inventory items",
)
def list_items():
    """
    TODO: Write a detailed docstring with:
    - A one-line summary
    - A blank line
    - A longer description explaining filters, sorting, or pagination (even if
      not implemented yet — document the intent)
    - Parameter descriptions
    """
    """
    1. This returns all items in the inventory. 
    2. items are returned as entered. additional features like filtering by category or price will be added.
    """ 
    return items

# TODO: Implement POST / with:
# - Detailed docstring
# - response_model=ItemResponse
# - status_code=201
# - responses={} documenting additional status codes (422, 409)
#
# Key concept: The responses={} parameter on an endpoint adds non-default
# response codes to the OpenAPI schema. Clients and API consumers see these
# in the Swagger "Responses" section, even though FastAPI doesn't validate them.
@router.post(
    "/",
    response_model=ItemResponse,
    status_code=201,
    responses={
        201:{
            "description": "Item created successfully. Returns the created item with server-assigned id."
        },
        409: {
            "description": "Item with this name exists. Please rename."
        },
        422: {
            "description": "Validation Error. Check request body for missing or invalid fields."
        },
    },
)
def create_item(item: ItemCreate):
    """
    TODO: Write a detailed docstring explaining:
    - What the endpoint does
    - What the request body should contain
    - What response codes are possible (201, 409, 422)
    """
    pass  # TODO: implement
    global _next_id
    for existing in items:
        if existing["name"].lower() == item.name.lower():
            raise HTTPException(status_code=409, detail=f"Item '{item.name}' already exists")
    new_item = {"id": _next_id, **item.model_dump()}
    items.append(new_item)
    _next_id += 1
    return new_item


# TODO: Implement GET /{item_id} with a good docstring and responses parameter
@router.get(
    "/{item_id}",
    response_model=ItemResponse,
    summary="Get a single item by ID",
    responses={
        200: {"description": "Item found"},
        404: {"description": "Item not found — check the item_id"},
    },
)
def get_item(item_id: int):
    """
    Returns a single inventory item by its integer ID.

    - **item_id**: The  identifier assigned when created.

    Returns **404** if no item with that ID exists.
    """
    for item in items:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail=f"Item {item_id} not found")