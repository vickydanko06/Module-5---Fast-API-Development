# exercises/student-crud/app/routers/students.py
# L6 — Full CRUD for students

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from typing import Optional

from app.schemas.student import StudentCreate, StudentUpdate, StudentPatch, StudentResponse
from app.models.student import Student
from app.database import get_db

router = APIRouter()

@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    """
    Creates a new student.
"""

    db_student = Student(**student.model_dump())
    try:
        db.add(db_student)
        db.commit()
        db.refresh(db_student)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = "Email already exists")
    return db_student


@router.get("/", response_model=list[StudentResponse])
def list_students(
    major: Optional[str] = Query(None),
    min_gpa: Optional[float] = Query(None, ge=0.0, le=4.0),
    db: Session = Depends(get_db),
):
    """
    Returns students, optionally filtered by major and/or minimum GPA.
"""
    query=db.query(Student)
    if major:
        query = query.filter(Student.major.ilike(f"%{major}%"))
    if min_gpa is not None:
        query = query.filter(Student.gpa >= min_gpa)
    return query.all()


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    """Returns a single student by ID."""
    pass  # TODO: implement
    student = db.get(Student, student_id)

    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found",
        )

    return student

@router.put("/{student_id}", response_model=StudentResponse)
def replace_student(student_id: int, student: StudentUpdate, db: Session = Depends(get_db)):
    """Fully replaces a student record."""

    # 1. Find the existing student
    db_student = db.get(Student, student_id)

    # 2. Return 404 if they don't exist
    if db_student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found",
        )

    # 3. Convert incoming Pydantic data to a dictionary
    update_data = student.model_dump()

    # 4. Replace the database values
    for field, value in update_data.items():
        setattr(db_student, field, value)

    # 5. Save changes
    try:
        db.commit()
        db.refresh(db_student)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists",
        )

    # 6. Return updated student
    return db_student

@router.patch("/{student_id}", response_model=StudentResponse)
def patch_student(student_id: int, student: StudentPatch, db: Session = Depends(get_db)):
    """
    Partially updates a student (only fields sent are changed).
    """
    pass  # TODO: implement
    db_student = db.get(Student, student_id)
    if db_student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found",
        )
    update_data = student.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_student, field, value)
    db.commit()
    db.refresh(db_student)
    return db_student

# TODO: DELETE /students/{student_id} — delete and return confirmation
@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    """
    Deletes a student by ID.

    TODO: Find student, raise 404 if missing, db.delete(student), db.commit().
    Return a success message dict.
    """
    pass  # TODO: implement
    db_student = db.get(Student, student_id)
    if db_student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found",
        )
    db.delete(db_student)
    db.commit()
    return {"message": "Student deleted successfully"}