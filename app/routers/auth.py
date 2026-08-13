from fastapi import APIRouter, HTTPException
from app.core.database import SessionLocal
from app.models.user import User
from app.schemas.auth import SignupRequest, LoginRequest, TokenResponse
from app.core.security import hash_password, verify_password, create_access_token

router = APIRouter()

@router.post("/auth/signup", response_model=TokenResponse)
def signup(payload: SignupRequest):
    db = SessionLocal()
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        db.close()
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(email=payload.email, hashed_password= hash_password(payload.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    user_id = user.id
    db.close()

    token = create_access_token(user_id)
    return TokenResponse(access_token=token)

@router.post("/auth/login", response_model=TokenResponse)
def login(payload: LoginRequest):
    db = SessionLocal()
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        db.close()
        raise HTTPException(status_code=401, details="Invalid Credentials")

    user_id = user.id
    db.close()

    token = create_access_token(user_id)
    return TokenResponse(access_token=token)