from app.core.database import SessionLocal
from app.models import Chunk, Document
from app.services.embeddings import embed_text
from app.services.pdf_loader import extract_text
from app.services.chunker import chunk_text

def ingest_pdf(file_path: str, filename: str, owner_id: int) -> tuple[int, int]:
    text = extract_text(file_path)
    chunks = chunk_text(text)

    db = SessionLocal()
    doc = Document(filename= filename, owner_id= owner_id)
    db.add(doc)
    db.commit()
    db.refresh(doc)
    document_id = doc.id

    for c in chunks:
        vector = embed_text(c)
        db.add(Chunk(text=c, embedding=vector, document_id=document_id))

    db.commit()
    db.close()

    return document_id, len(chunks)