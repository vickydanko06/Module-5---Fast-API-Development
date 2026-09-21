# exercises/student-crud/app/models/student.py
# L6 — Student ORM model

from sqlalchemy import String, Float, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Student(Base):
    """SQLAlchemy model for the students table."""
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100),nullable=False)
    email: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    major: Mapped[str | None] = mapped_column(String(100), nullable=True)
    gpa: Mapped[float | None] = mapped_column(Float, nullable=True)

   