from fastapi import APIRouter
from app.schemas.rag import AskDocumentRequest, AskDocumentResponse
from app.services.retrieval import search_similar
from app.services.llm import ask_with_context

router = APIRouter()

@router.post("/ask-document", response_model=AskDocumentResponse)
def ask_document(payload: AskDocumentRequest):
    chunks = search_similar(payload.question, document_id = payload.document_id, top_k=3)
    answer = ask_with_context(payload.question, chunks)

    return AskDocumentResponse(answer=answer, source=chunks)