# exercises/database-notes/app/models/note.py
# L5 — SQLAlchemy 2.0 Note model
#
# Your task: Define the Note ORM model using SQLAlchemy 2.0 syntax.

from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class Note(Base):
    """SQLAlchemy model for the notes table."""
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200),nullable=False)
    content: Mapped[str] = mapped_column(Text,nullable=False)
    category: Mapped[Optional[str]] = mapped_column(String(50),nullable=True)
    is_pinned: Mapped[bool] = mapped_column(Boolean,default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default = datetime.utcnow)
