# exercises/validated-contacts/app/routers/contacts.py
# L3 — Contact book endpoints

# TODO: Import APIRouter, HTTPException, Query, status from fastapi
from fastapi import APIRouter, HTTPException, Query, status

# TODO: Import the schemas you defined
from app.schemas.contact import ContactCreate, ContactUpdate, ContactResponse, ContactCategory

from typing import Optional
from datetime import datetime

router = APIRouter()

# In-memory storage
contacts: list[dict] = []
_next_id = 1


# TODO: POST / — create a new contact
# - Accept a ContactCreate body
# - Assign an id and created_at timestamp
# - Append to contacts list
# - Return ContactResponse with status 201
@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
def create_contact(contact: ContactCreate):
    """
    Creates a new contact.

    TODO:
    1. Build a dict from contact.model_dump()
    2. Add "id" and "created_at" keys
    3. Append to contacts
    4. Return the dict (FastAPI will validate it against ContactResponse)
    """
    pass  # TODO: implement
    global _next_id
    new_contact ={
        "id": _next_id,
        **contact.model_dump(),
        "created_at": datetime.now().isoformat()
    }
    contacts.append(new_contact)
    _next_id += 1
    return new_contact


# TODO: GET / — list all contacts, with optional category filter
# Query param: category (optional ContactCategory)
@router.get("/", response_model=list[ContactResponse])
def list_contacts(category: Optional[ContactCategory] = Query(None)):
    """
    Returns all contacts.
    Optionally filter by category using ?category=work

    TODO: Return contacts filtered by category if provided, otherwise all.
    """
    pass  # TODO: implement
    if category:
        return [c for c in contacts if c["category"] == category.value]
    return contacts


# TODO: GET /{contact_id} — get a single contact by id
@router.get("/{contact_id}", response_model=ContactResponse)
def get_contact(contact_id: int):
    """
    Returns a single contact by ID.

    TODO: Search contacts, raise 404 if not found
    """
    pass  # TODO: implement
    for contact in contacts:
        if (contact["id"] == contact_id):
            return contact
    raise HTTPException(status_code = 404, detail = "contact not found" )

# TODO: PATCH /{contact_id} — partially update a contact
# Use contact_data.model_dump(exclude_unset=True) to only update provided fields
@router.patch("/{contact_id}", response_model=ContactResponse)
def update_contact(contact_id: int, contact_data: ContactUpdate):
    """
    Partially updates a contact.

    Key concept: model_dump(exclude_unset=True) returns only the fields the
    client actually sent, so fields they didn't include are left unchanged.

    TODO:
    1. Find the contact (raise 404 if missing)
    2. Get the update dict with exclude_unset=True
    3. Update only those keys on the stored contact
    4. Return the updated contact
    """
    pass  # TODO: implements
    for contact in contacts:
        if contact["id"] == contact_id:
            updates = contact_data.model_dump(exclude_unset=True)
            contact.update(updates)
            return contact

    raise HTTPException(status_code=404, detail="contact not found")
