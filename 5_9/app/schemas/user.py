# exercises/auth-system/app/schemas/user.py
# L8 — User schemas

from pydantic import BaseModel, ConfigDict, Field


class UserCreate(BaseModel):
    """Schema for user registration."""
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    """Schema for returning user data (no password fields)."""
    id: int
    username: str
    email: str

    model_config = ConfigDict(from_attributes=True)


# TODO: Define TokenResponse — returned after successful login
# Fields: access_token (str), token_type (str, default "bearer")
class TokenResponse(BaseModel):
    """Schema for the JWT response."""
    access_token: str
    token_type: str = "bearer"
