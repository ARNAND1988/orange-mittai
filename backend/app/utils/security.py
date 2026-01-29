from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from app.config import SECRET_KEY, ALGORITHM

# --- Password hashing ---
# Use sha256_crypt to avoid bcrypt 72-byte limit
pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)  # no truncation needed

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# --- JWT token ---
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day

def create_access_token(
        data: dict,
        expires_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES
):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

