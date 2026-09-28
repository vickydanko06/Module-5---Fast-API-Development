# exercises/auth-system/app/models/user.py
# L8 — User ORM model

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class User(Base):
    """SQLAlchemy model for the users table."""
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column(String)
