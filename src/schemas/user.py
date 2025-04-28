from typing import Optional, Annotated
from pydantic import BaseModel, Field, EmailStr
from src.enum.preference_enum import GenreEnum

class UserBase(BaseModel):
    name: Annotated[str, Field(max_length=255)]
    email: EmailStr
    preference: Optional[GenreEnum] = None

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    name: Optional[Annotated[str, Field(max_length=255)]] = None
    preference: Optional[GenreEnum] = None

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True
