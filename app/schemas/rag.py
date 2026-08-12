from pydantic import BaseModel

class AskDocumentRequest(BaseModel):
    question: str
    document_id: int

class AskDocumentResponse(BaseModel):
    answer: str
    source: list[str]