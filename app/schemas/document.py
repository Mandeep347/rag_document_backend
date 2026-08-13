from pydantic import BaseModel
from datetime import datetime

class UploadDocumentResponse(BaseModel):
    document_id: int
    filename: str
    chunks_created: int

class DocumentListItem(BaseModel):
    id: int
    filename: str
    status: str
    error_message: str
    created_at: datetime

    class Config:
        from_attributes = True