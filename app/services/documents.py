from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.document import Document

def verify_document_owner(document_id: int, user_id: int, db: Session) -> None:
    doc = db.query(Document).filter(Document.id == document_id).first()
    if doc.status != "ready":
        raise HTTPException(status_code=400, detail=f"Document not ready (status: {doc.status})")
    db.close()

    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    if doc.owner_id != user_id:
        raise HTTPException(status_code=403, detail="Not your document")