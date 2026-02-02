from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import random

from app.database import get_db
from app.models.user import User, PasswordReset
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.user_schema import UserCreate, UserRead
from app.schemas.auth_schema import (
    ForgotPasswordRequest,
    ResetPasswordRequest,
    LoginRequest,
)
from app.utils.security import (
    hash_password,
    verify_password,
    create_access_token,
)

router = APIRouter()

@router.post("/register", response_model=UserRead)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user = User(
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        phone=user.phone,
        hashed_password=hash_password(user.password),
        is_admin=False,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

# ---- Login endpoint ----
@router.post("/login")
def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({
        "id": str(user.id),
        "email": user.email,
        "is_admin": user.is_admin,
    })

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_admin": user.is_admin,
        },
    }
@router.post("/forgot-password")
def forgot_password(
        payload: ForgotPasswordRequest,
        db: Session = Depends(get_db),
):
    if not payload.email and not payload.phone:
        raise HTTPException(
            status_code=400,
            detail="Email or phone is required",
        )

    if payload.email:
        user = db.query(User).filter(User.email == payload.email).first()
        channel = "EMAIL"
        identifier = payload.email
    else:
        user = db.query(User).filter(User.phone == payload.phone).first()
        channel = "PHONE"
        identifier = payload.phone

    # Prevent user enumeration
    if not user:
        return {"message": "If account exists, OTP will be sent"}

    otp = str(random.randint(100000, 999999))

    reset = PasswordReset(
        user_id=user.id,
        otp=otp,
        channel=channel,
        expires_at=datetime.utcnow() + timedelta(minutes=10),
    )

    db.add(reset)
    db.commit()

    # 🔔 Replace with real services
    if channel == "EMAIL":
        print(f"[EMAIL OTP to {identifier}]: {otp}")
    else:
        print(f"[SMS OTP to {identifier}]: {otp}")

    return {"message": "If account exists, OTP will be sent"}

@router.post("/reset-password")
def reset_password(
        payload: ResetPasswordRequest,
        db: Session = Depends(get_db),
):
    user = (
        db.query(User)
        .filter(
            (User.email == payload.identifier)
            | (User.phone == payload.identifier)
        )
        .first()
    )

    if not user:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    reset = (
        db.query(PasswordReset)
        .filter(
            PasswordReset.user_id == user.id,
            PasswordReset.otp == payload.otp,
            PasswordReset.is_used == False,
            PasswordReset.expires_at > datetime.utcnow(),
            )
        .order_by(PasswordReset.created_at.desc())
        .first()
    )

    if not reset:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")

    user.hashed_password = hash_password(payload.new_password)
    reset.is_used = True

    db.commit()

    return {"message": "Password reset successful"}

