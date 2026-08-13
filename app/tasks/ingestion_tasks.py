from app.core.celery_app import celery_app
from app.services.ingestion import ingest_pdf

@celery_app.task
def ingest_pdf_task(file_path: str, filename: str):
    document_id, chunk_count = ingest_pdf(file_path, filename)
    return {
        "document_id": document_id, 
        "chunk_created": chunk_count,
    }