from fastapi import FastAPI, Request
from app.routers import rag
from app.routers import documents
from app.routers import auth

from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.core.limiter import limiter

app = FastAPI(title="My API")

print("=== BEFORE ASSIGNMENT ===")
print(f"app.state type: {type(app.state)}")
print(f"app.state id: {id(app.state)}")
print(f"app.state._state: {app.state._state}")
print(f"hasattr(app.state, 'limiter'): {hasattr(app.state, 'limiter')}")

app.state.limiter = limiter

print("=== AFTER ASSIGNMENT ===")
print(f"app.state._state: {app.state._state}")
print(f"hasattr(app.state, 'limiter'): {hasattr(app.state, 'limiter')}")
print(f"app.state.limiter is limiter: {app.state.limiter is limiter}")

app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/_debug")
def debug(request: Request):
    return {
        "app_id": id(request.app),
        "has_limiter": hasattr(request.app.state, "limiter"),
        "same_app": id(request.app) == id(app)
    }

app.include_router(rag.router)
app.include_router(documents.router)
app.include_router(auth.router)
