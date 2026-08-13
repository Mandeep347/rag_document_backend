from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import decode_access_token

bearer_schema = HTTPBearer()

def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(bearer_schema)) -> int:
    token = credentials.credentials
    try:
        return decode_access_token(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Inavlid or expired access token")
    