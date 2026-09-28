# exercises/auth-system/app/routers/auth.py
# L8 — Auth endpoints

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.schemas.user import UserCreate, UserResponse, TokenResponse
from app.models.user import User
from app.database import get_db

from app.auth import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter()



@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    Registers a new user.
    """
    existing = db.query(User).filter(
    (User.username == user.username) | (User.email == user.email)
).first()
    if existing:
        raise HTTPException(status_code = 409, detail="email already registered")
    user = User(
        username = user.username,
        email=user.email,
        hashed_password = hash_password(user.password),
        )
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


# TODO: POST /token — login, return JWT
# FastAPI provides OAuth2PasswordRequestForm which parses username + password
# from a form body (the standard OAuth2 format expected by Swagger's Authorize).
@router.post("/token", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Authenticates user credentials and returns a JWT access token.

    Key concept: OAuth2PasswordRequestForm parses a form-encoded body with
    fields 'username' and 'password'. This is the standard format that lets
    the Swagger UI 'Authorize' button work out of the box.

    TODO:
    1. Look up user by username
    2. verify_password(form_data.password, user.hashed_password)
    3. create_access_token({"sub": user.username})
    4. Return TokenResponse
    """
    user = db.query(User).filter(
        User.username == form_data.username
    ).first()

    if not user or not verify_password(
        form_data.password,
        user.hashed_password,
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
        )

    access_token = create_access_token({"sub": user.username})

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
    )

# TODO: GET /me — return the currently authenticated user
# Use Depends(get_current_user) to extract the user from the JWT
@router.get("/me", response_model=UserResponse)
def get_me(current_user=Depends(get_current_user)):  # TODO: replace None with get_current_user
    """
    Returns the currently authenticated user.

    Key concept: Depends(get_current_user) runs the dependency before the
    endpoint. If the token is invalid or missing, get_current_user raises a
    401 and this function never executes.
    """
    return current_user


# TODO: Add at least one more protected endpoint (e.g., GET /profile or GET /dashboard)
@router.get("/profile")
def get_profile(current_user=Depends(get_current_user)):
    """
    Returns a protected profile message for the authenticated user.
    """
    return {
        "message": f"Welcome, {current_user.username}!",
        "username": current_user.username,
        "email": current_user.email,
    }