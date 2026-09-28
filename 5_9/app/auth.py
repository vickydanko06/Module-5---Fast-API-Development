# exercises/auth-system/app/auth.py
# L8 — JWT utility functions
#
# Your task: Implement password hashing and JWT creation/verification.

# TODO: Import CryptContext from passlib.context
from passlib.context import CryptContext

# TODO: Import jwt from jose, and JWTError
from jose import jwt, JWTError

# TODO: Import Depends, HTTPException, status from fastapi
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.database import get_db

# ── Config ─────────────────────────────────────────────────────────────────────
# In production, SECRET_KEY should come from an environment variable.
# Never hard-code secrets in real code!
SECRET_KEY = "dev-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# TODO: Create the passlib CryptContext
# schemes=["bcrypt"] tells passlib to use bcrypt for hashing
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
schemes = ["bcrypt"]
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2PasswordBearer sets up the token extraction from the Authorization header.
# tokenUrl tells Swagger where to POST for a token (used by the "Authorize" button).
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


# TODO: Implement hash_password(password: str) -> str
# Use pwd_context.hash(password)
def hash_password(password: str) -> str:
    """Returns the bcrypt hash of the given plain-text password."""
    return pwd_context.hash(password)


# TODO: Implement verify_password(plain: str, hashed: str) -> bool
# Use pwd_context.verify(plain, hashed)
def verify_password(plain: str, hashed: str) -> bool:
    """Returns True if plain matches the hashed password."""
    return pwd_context.verify(plain, hashed)


# TODO: Implement create_access_token(data: dict) -> str
# 1. Copy data into a new dict
# 2. Add "exp" key: datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
# 3. Return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#
# Key concept: JWTs contain a payload (claims) signed with the SECRET_KEY.
# Anyone can decode the payload, but only someone with SECRET_KEY can create
# a valid signature. The "exp" claim makes the token expire automatically.
def create_access_token(data: dict) -> str:
    """Creates a signed JWT access token."""
    to_encode=data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# TODO: Implement get_current_user(token, db) — a FastAPI dependency
# 1. Try to decode the token: jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
# 2. Extract "sub" (subject = username) from the payload
# 3. Look up the user in the DB
# 4. Raise 401 if any step fails
#
# Key concept: Depends(get_current_user) on an endpoint means FastAPI will
# call this function first and inject its return value. If the function raises
# an exception, the endpoint never runs — the error is returned instead.
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    """
    Dependency that extracts and validates the JWT, returning the current user.
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        username = payload.get("sub")

        if username is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    from app.models.user import User

    user = db.query(User).filter(User.username == username).first()

    if user is None:
        raise credentials_exception

    return user