# exercises/custom-errors/app/routers/students.py
# L7 — Student endpoints using custom exceptions

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from app.exceptions import NotFoundError, DuplicateError


from app.schemas.student import StudentCreate, StudentResponse
from app.models.student import Student
from app.database import get_db
# TODO: Import your custom exception classes
# from app.exceptions import NotFoundError, DuplicateError

router = APIRouter()


# TODO: Implement POST / — create a student
# Instead of raising HTTPException, raise DuplicateError when the email exists
@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    """
    Creates a student. Raises DuplicateError (not HTTPException) if email taken.

    TODO:
    1. Check for existing email — raise DuplicateError("Email X already registered")
    2. Create, add, commit, refresh, return
    """
    
    existing = db.scalar(
        select(Student).where(Student.email == student.email)
    )

    if existing:
        raise DuplicateError(
            f"Email {student.email} already registered"
        )

    db_student = Student(
        name=student.name,
        email=student.email,
        major=student.major,
        gpa=student.gpa,
    )

    try:
        db.add(db_student)
        db.commit()
        db.refresh(db_student)
    except IntegrityError:
        db.rollback()
        raise DuplicateError("Email already registered")

    return db_student


# TODO: Implement GET /{student_id} — raise NotFoundError instead of HTTPException
@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    """
    Gets a student. Raises NotFoundError if not found.

    TODO: raise NotFoundError(f"Student {student_id} not found")
    """
    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        raise NotFoundError(f"Student {student_id} not found")

    return student


# TODO: Implement DELETE /{student_id}
@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    """Deletes a student. Raises NotFoundError if not found."""
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise NotFoundError(f"Student {student_id} not found")
    db.delete(student)
    db.commit()
    return {"message": f"Student {student_id} deleted"}