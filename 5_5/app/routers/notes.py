
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.note import Note
from app.schemas.note import NoteCreate, NoteResponse


router = APIRouter()


@router.post("/", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def create_note(note: NoteCreate, db: Session = Depends(get_db)):
    """
    Creates a new note in the database.
    """
    db_note = Note(**note.model_dump())

    db.add(db_note)
    db.commit()
    db.refresh(db_note)

    return db_note


@router.get("/", response_model=list[NoteResponse])
def list_notes(
    category: Optional[str] = Query(None),
    is_pinned: Optional[bool] = Query(None),
    db: Session = Depends(get_db),
):
    """
    Returns notes, optionally filtered by category and/or pinned status.
    """

    query = select(Note)

    if category:
        query = query.where(Note.category.ilike(f"%{category}%"))

    if is_pinned is not None:
        query = query.where(Note.is_pinned == is_pinned)

    return db.execute(query).scalars().all()

@router.get("/{note_id}", response_model=NoteResponse)
def get_note(note_id: int, db: Session = Depends(get_db)):
    """
    Returns a single note by ID.
    """
    note = db.get(Note, note_id)

    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",
        )

    return note

@router.delete("/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    """
    Deletes a note by ID.

    TODO: Find the note, raise 404 if missing, db.delete(note), db.commit().
    Return a success message dict.
    """
    note = db.get(Note, note_id)
        
    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",
        )
    db.delete(note)
    db.commit()

    return {"message": "Note deleted successfully"}

