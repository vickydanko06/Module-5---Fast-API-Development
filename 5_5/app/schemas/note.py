# exercises/database-notes/app/schemas/note.py
# L5 — Pydantic schemas for Note

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class NoteCreate(BaseModel):
    """Schema for creating a new note."""
    title: str = Field(min_length=1, max_length=200)
    content: str 
    category: Optional[str] = Field(default = None,max_length=50)
    is_pinned: bool = Field(default=False)

class NoteResponse(NoteCreate):
    """Schema for returning note data in API responses."""
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)