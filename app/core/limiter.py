from slowapi import Limiter
from slowapi.util import get_remote_address
from app.core.config import settings

def get_user_id_or_ip(request):
    return getattr(request.state, "user_id", None) or get_remote_address(request)

limiter = Limiter(key_func=get_user_id_or_ip, storage_uri= settings.redis_url+"1")