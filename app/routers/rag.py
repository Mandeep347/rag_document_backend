from fastapi import APIRouter, Depends, Request
from app.schemas.rag import AskDocumentRequest, AskDocumentResponse
from app.services.retrieval import search_similar
from app.services.llm import ask_with_context, ask_with_context_stream
from app.core.deps import get_current_user_id
from app.core.limiter import limiter
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.core.database import get_db


router = APIRouter()

@router.post("/ask-document", response_model=AskDocumentResponse)
@limiter.limit("10/minute")
def ask_document(request: Request, payload: AskDocumentRequest, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    chunks = search_similar(user_id, payload.question, document_id = payload.document_id, db=db, top_k=3)
    answer = ask_with_context(payload.question, chunks)
    return AskDocumentResponse(answer=answer, source=chunks)

@router.post("/ask-document/stream")
@limiter.limit("10/minute")
def ask_document_stream(request: Request, payload: AskDocumentRequest, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    chunks = search_similar(user_id=user_id, query=payload.question, document_id=payload.document_id, db=db)

    def event_generator():
        for token in ask_with_context_stream(payload.question, chunks):
            yield token

    return StreamingResponse(event_generator(), media_type="text/plain")