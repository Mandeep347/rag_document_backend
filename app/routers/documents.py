import os
from fastapi import APIRouter, Depends, UploadFile, File, Request, HTTPException
from app.schemas.document import DocumentListItem
from app.tasks.ingestion_tasks import ingest_pdf_task
from celery.result import AsyncResult
from app.core.celery_app import celery_app
from app.core.deps import get_current_user_id
from app.core.limiter import limiter
from typing import List
from app.models import Document, Chunk
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.documents import verify_document_owner
from app.services.storage import upload_file, delete_file

router = APIRouter()

UPLOAD_DIR = "app/uploaded_files"
ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}
MAX_FILE_SIZE = 25 * 1024 * 1024
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/documents/upload")
@limiter.limit("3/minute")
def upload_document(request: Request, file: UploadFile = File(...), user_id: int = Depends(get_current_user_id)):
    ext = file.filename.lower().rsplit(".", 1)[-1] if "." in file.filename else ""
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail= f"Unsupported file type: .{ext}")

    file_bytes = file.file.read()
    if len(file_bytes) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File exceeds 25MB limit")

    storage_path = f"{user_id}/{file.filename}"
    upload_file(file_bytes, storage_path)

    task = ingest_pdf_task.delay(storage_path, file.filename, user_id)
    return {"task_id": task.id, "status": "processing"}

@router.get("/documents/status/{task_id}")
def get_task_status(task_id: str):
    result = AsyncResult(task_id, app=celery_app)
    if result.state == "PENDING":
        return {"status": "pending"}
    elif result.state == "SUCCESS":
        return {"status": "done", "result": result.result}
    elif result.state == "FAILURE":
        return {"status": "failed", "error": str(result.result)}
    return {"status": result.state}

@router.get("/documents", response_model=List[DocumentListItem])
def list_document(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    docs = db.query(Document).filter(Document.owner_id == user_id).order_by(Document.created_at.desc()).all()
    db.close()
    return docs

@router.delete("/documents/{document_id}")
def delete_document(document_id: int, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == document_id).first()
    verify_document_owner(document_id, user_id, db)

    storage_path = f"{user_id}/{doc.filename}"
    delete_file(storage_path)

    db.query(Chunk).filter(Chunk.document_id == document_id).delete()
    db.query(Document).filter(Document.id == document_id).delete()
    db.commit()
    return {"status": "deleted", "document_id": document_id}