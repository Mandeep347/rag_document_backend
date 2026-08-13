from fastapi import APIRouter, HTTPException, Request, Depends
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.auth import SignupRequest, LoginRequest, TokenResponse
from app.core.security import hash_password, verify_password, create_access_token
from app.core.limiter import limiter
from app.core.database import get_db

router = APIRouter()

@router.post("/auth/signup", response_model=TokenResponse)
@limiter.limit("2/minute")
def signup(request: Request, payload: SignupRequest, db: Session = Depends(get_db)):
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
@limiter.limit("3/minute")
def login(request: Request, payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        db.close()
        raise HTTPException(status_code=401, detail="Invalid Credentials")

    user_id = user.id
    db.close()

    token = create_access_token(user_id)
    return TokenResponse(access_token=token)