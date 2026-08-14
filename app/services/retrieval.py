from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.chunk import Chunk
from app.services.embeddings import embed_text
from app.services.documents import verify_document_owner

def search_similar(user_id: int, query: str, document_id: int, db: Session, top_k: int = 3):
    verify_document_owner(document_id, user_id, db)

    query_vector = embed_text([query])[0]
    results = db.scalars(
        select(Chunk)
        .where(Chunk.document_id == document_id)
        .order_by(Chunk.embedding.cosine_distance(query_vector))
        .limit(top_k)
    ).all()
    db.close()
    return [r.text for r in results]