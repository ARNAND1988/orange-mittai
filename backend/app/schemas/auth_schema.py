from pydantic import BaseModel, EmailStr, constr
from typing import Optional

class ForgotPasswordRequest(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

class ResetPasswordRequest(BaseModel):
    identifier: str  # email or phone
    otp: str
    new_password: constr(min_length=6, max_length=72)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RegisterRequest(BaseModel):
    email: str
    first_name: str
    last_name: str
    phone: str
    password: str