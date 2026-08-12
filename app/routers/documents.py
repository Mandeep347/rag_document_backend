import shutil
import os
from fastapi import APIRouter, UploadFile, File
from app.schemas.document import UploadDocumentResponse
from app.services.ingestion import ingest_pdf

router = APIRouter()

UPLOAD_DIR = "app/uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/documents/upload", response_model=UploadDocumentResponse)
def upload_document(file: UploadFile = File(...)):
    save_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    document_id, chunk_count = ingest_pdf(save_path, file.filename)

    return UploadDocumentResponse(
        document_id= document_id,
        filename= file.filename,
        chunks_created= chunk_count,
    )