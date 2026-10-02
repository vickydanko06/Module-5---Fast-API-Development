# exercises/polished-docs/app/schemas/item.py
# L12 — Item schema with documentation

from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


# TODO: Define an Item schema with:
#   - name (str, 1-100 chars)
#   - description (optional str, max 500)
#   - price (float, > 0)
#   - category (str)
#
# Add model_config = ConfigDict(json_schema_extra={"example": {...}})
# so that the Swagger UI shows a pre-filled example in the request body.
#
# Key concept: json_schema_extra adds an "example" to the OpenAPI schema.
# Swagger shows this in the "Try it out" panel, making it much easier for
# API consumers to understand what a valid request looks like.
class Item(BaseModel):
    """An item in the inventory."""
    name: str=Field(min_length=1,max_length=100)
    description: Optional[str]=Field(default=None,max_length=500)
    price: float=Field(gt=0)
    category:str

    model_config = ConfigDict(json_schema_extra={"example":{"name":"Example Item","description":"This is an example item","price":9.99,"category":"Example Category"}})

class ItemCreate(BaseModel):
    """Schema for creating an item."""
    name: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    price: float = Field(gt=0)
    category: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Example Item",
                "description": "This is an example item",
                "price": 9.99,
                "category": "Example Category",
            }
        }
    )


class ItemResponse(ItemCreate):
    """Schema returned to clients — includes server-assigned id."""
    

    id: int

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Example Item",
                "description": "This is an example item",
                "price": 9.99,
                "category": "Example Category",
            }
        }
    )