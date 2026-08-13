from fastapi import APIRouter, Depends
from app.schemas.rag import AskDocumentRequest, AskDocumentResponse
from app.services.retrieval import search_similar
from app.services.llm import ask_with_context
from app.core.deps import get_current_user_id

router = APIRouter()

@router.post("/ask-document", response_model=AskDocumentResponse)
def ask_document(payload: AskDocumentRequest, user_id: int = Depends(get_current_user_id)):
    chunks = search_similar(user_id, payload.question, document_id = payload.document_id, top_k=3)
    answer = ask_with_context(payload.question, chunks)
    return AskDocumentResponse(answer=answer, source=chunks)