# exercises/validated-contacts/app/schemas/contact.py
# L3 — Pydantic schemas for Contact
#
# Your task: Define three Pydantic v2 schemas for the contact book API.
# Use Field() for constraints, a custom validator for email, and an Enum
# for the category field.

# TODO: Import BaseModel, Field, field_validator from pydantic
from pydantic import BaseModel, Field, field_validator, ConfigDict

# TODO: Import Optional from typing
from typing import Optional

# TODO: Import Enum from enum
from enum import Enum

# TODO: Define a ContactCategory Enum with values: personal, work, family
# Hint:
# class ContactCategory(str, Enum):
#     personal = "personal"
#     ...
class ContactCategory(str, Enum):
    pass  # TODO: add enum members
    """only allow these contact categories"""
    personal = "personal"
    work = "work"
    family = "family"


# TODO: Define ContactCreate schema
# Fields:
#   first_name: str, 1–50 chars
#   last_name:  str, 1–50 chars
#   email:      str, must contain "@" (validate with @field_validator)
#   phone:      optional str, 10–15 chars
#   category:   ContactCategory (required)
#
# Key concept: Field(min_length=..., max_length=...) adds validation constraints
# that FastAPI will enforce automatically and document in the OpenAPI schema.
class ContactCreate(BaseModel):
    """Schema for creating a new contact."""
    # TODO: add fields with Field() constraints
    pass  # TODO: implement
    first_name: str=Field(min_length=1,max_length=50)#first name contraints
    last_name: str=Field(min_length=1,max_length=50)#last name constraints
    email: str
    @field_validator("email")
    @classmethod
    def email_must_contain_at(cls,v):#email validation
        if "@" not in v:
            raise ValueError("email must contain @")
        return v
    phone: Optional[str] = Field(min_length=10,max_length=15)
    category: ContactCategory 

    # TODO: Add a @field_validator("email") that raises ValueError if "@" not in value
    # Hint:
    # @field_validator("email")
    # @classmethod
    # def email_must_contain_at(cls, v):
    #     if "@" not in v:
    #         raise ValueError("email must contain @")
    #     return v


# TODO: Define ContactUpdate schema
# Same fields as ContactCreate but ALL are Optional
# This lets PATCH requests update only the fields provided
#
# Key concept: Separate schemas for create vs update mean you don't have to
# make everything optional on the create schema, preserving required-field
# validation for new contacts.
class ContactUpdate(BaseModel):
    """Schema for partially updating a contact (all fields optional)."""
    # TODO: add optional versions of all ContactCreate fields
    pass  # TODO: implement
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    category: Optional[ContactCategory] = None


# TODO: Define ContactResponse schema
# Inherits all ContactCreate fields, adds:
#   id:         int
#   created_at: str
#
# Key concept: The response schema defines WHAT gets sent back to clients.
# Keeping it separate means you control exactly which fields are exposed
# (e.g., you can exclude internal fields like hashed_password).
class ContactResponse(ContactCreate):
    """Schema for returning contact data in API responses."""
    # TODO: add id and created_at fields
    pass  # TODO: implement

    # TODO: Add model_config = ConfigDict(from_attributes=True)
    # (needed when building from ORM objects later in L5+)
    id: int #system generated
    created_at: str #system generated

    model_config = ConfigDict(from_attributes=True)