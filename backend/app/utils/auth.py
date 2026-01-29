from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User, PasswordReset
from app.config import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
    )
    try:
        print("🔥 VERIFYING TOKEN:", token)
        print("token:", token, SECRET_KEY, ALGORITHM)
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        print("JWT payload:", payload)
        user_id: int = payload.get("id")
        print("user id ")
        if user_id is None:
            raise credentials_exception
    except JWTError as e:
        print("JWT decode error:", e)
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise credentials_exception
    return user

def generate_otp():
    return str(random.randint(100000, 999999))

def otp_expired(reset: PasswordReset):
    return reset.expires_at < datetime.utcnow()
