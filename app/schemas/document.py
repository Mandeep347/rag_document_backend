from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UploadDocumentResponse(BaseModel):
    document_id: int
    filename: str
    chunks_created: int

class DocumentListItem(BaseModel):
    id: int
    filename: str
    status: str
    error_message: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True