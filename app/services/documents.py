from fastapi import HTTPException
from app.core.database import SessionLocal
from app.models.document import Document

def verify_document_owner(document_id: int, user_id: int) -> None:
    db = SessionLocal()
    doc = db.query(Document).filter(Document.id == document_id).first()
    db.close()

    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    if doc.owner_id != user_id:
        raise HTTPException(status_code=403, detail="Not your document")