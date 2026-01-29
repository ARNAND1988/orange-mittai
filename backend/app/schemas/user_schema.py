from pydantic import BaseModel, EmailStr, constr
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None


class UserCreate(UserBase):
    password: constr(min_length=6, max_length=72)

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None

class UserRead(UserBase):
    id: int
    is_active: bool
    is_admin: bool

    class Config:
        orm_mode = True
