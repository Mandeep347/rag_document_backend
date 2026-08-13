from fastapi import Request, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import decode_access_token

bearer_schema = HTTPBearer()

def get_current_user_id(request: Request, credentials: HTTPAuthorizationCredentials = Depends(bearer_schema)) -> int:
    token = credentials.credentials
    try:
        user_id = decode_access_token(token)
        request.state.user_id = user_id
        return user_id
    except Exception:
        raise HTTPException(status_code=401, detail="Inavlid or expired access token")
    