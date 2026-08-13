from app.core.database import SessionLocal
from app.models import Chunk, Document
from app.services.embeddings import embed_text
from app.services.text_extractor import extract_text
from app.services.chunker import chunk_text

def ingest_pdf(file_path: str, filename: str, owner_id: int) -> tuple[int, int]:
    db = SessionLocal()
    doc = Document(filename=filename, owner_id= owner_id, status="processing")
    db.add(doc)
    db.commit()
    db.refresh(doc)
    document_id = doc.id
    db.close()

    try:
        text = extract_text(file_path, filename)
        chunks = chunk_text(text)

        if not chunks:
            raise ValueError("No extractable text found in file")

        db = SessionLocal()
        for c in chunks:
            vector = embed_text(c)
            db.add(Chunk(text=c, embedding= vector, document_id=document_id))

        doc_row = db.query(Document).filter(Document.id == document_id).first()
        doc_row.status = "ready"
        db.commit()
        db.close()

        return document_id, len(chunks)

    except Exception as e:
        db = SessionLocal()
        doc_row = db.query(Document).filter(Document.id == document_id).first()
        doc_row.status = "failed"
        doc_row.error_message = str(e)
        db.commit()
        db.close()
        raise