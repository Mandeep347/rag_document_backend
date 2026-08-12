from pydantic import BaseModel

class UploadDocumentResponse(BaseModel):
    document_id: int
    filename: str
    chunks_created: int