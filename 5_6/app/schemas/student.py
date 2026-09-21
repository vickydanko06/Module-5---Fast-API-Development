# exercises/student-crud/app/schemas/student.py
# L6 — Pydantic schemas for Student

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class StudentCreate(BaseModel):
    """Schema for creating a student."""
    name: str
    email: str = Field(pattern=r".+@.+")
    major: Optional[str] = None
    gpa: Optional[float] = Field(default=None, ge=0, le=4)


class StudentUpdate(BaseModel):
    """Schema for fully replacing a student (PUT)."""
    name: Optional[str] = None
    email: Optional[str] = Field(default=None, pattern=r".+@.+")
    major: Optional[str] = None
    gpa: Optional[float] = Field(default=None, ge=0, le=4)


class StudentPatch(BaseModel):
    """Schema for partially updating a student (PATCH)."""
    name: Optional[str] = None
    email: Optional[str] = Field(default=None, pattern=r".+@.+")
    major: Optional[str] = None
    gpa: Optional[float] = Field(default=None, ge=0, le=4)


class StudentResponse(StudentCreate):
    """Schema for returning student data."""
    id: int

    model_config = ConfigDict(from_attributes=True)