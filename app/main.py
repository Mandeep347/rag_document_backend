from fastapi import FastAPI
from app.routers import rag
from app.routers import documents

app = FastAPI(title="My API")
app.include_router(rag.router)
app.include_router(documents.router)

