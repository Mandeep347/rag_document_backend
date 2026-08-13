from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password[:72])

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain[:72], hashed)

def create_access_token(user_id: int) -> str:
    expire = datetime.utcnow() + timedelta(hours= settings.expire_time)
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, settings.jwt_secret, algorithm= settings.algorithm)

def decode_access_token(token: str) -> int:
    payload = jwt.decode(token, settings.jwt_secret, algorithms= settings.algorithm)
    return int(payload["sub"])