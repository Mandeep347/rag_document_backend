from fastapi import FastAPI, Request
from app.routers import rag
from app.routers import documents
from app.routers import auth

from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.core.limiter import limiter

app = FastAPI(title="My API")

app.state.limiter = limiter

app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(rag.router)
app.include_router(documents.router)
app.include_router(auth.router)
