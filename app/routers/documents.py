import shutil
import os
from fastapi import APIRouter, Depends, UploadFile, File
from app.schemas.document import UploadDocumentResponse
from app.tasks.ingestion_tasks import ingest_pdf_task
from celery.result import AsyncResult
from app.core.celery_app import celery_app
from app.core.deps import get_current_user_id

router = APIRouter()

UPLOAD_DIR = "app/uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/documents/upload")
def upload_document(file: UploadFile = File(...), user_id: int = Depends(get_current_user_id)):
    save_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    task = ingest_pdf_task.delay(save_path, file.filename, user_id)

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