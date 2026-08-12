from fastapi import FastAPI
from app.routers import rag

app = FastAPI(title="My API")
app.include_router(rag.router)

