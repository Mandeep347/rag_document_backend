from app.core.database import SessionLocal
from app.models import Chunk, Document
from app.services.embeddings import embed_text
from app.services.text_extractor import extract_text
from app.services.chunker import chunk_text
import tempfile
import os
from app.services.storage import download_file

def ingest_pdf(storage_path: str, filename: str, owner_id: int) -> tuple[int, int]:
    db = SessionLocal()
    doc = Document(filename=filename, owner_id= owner_id, status="processing")
    db.add(doc)
    db.commit()
    db.refresh(doc)
    document_id = doc.id
    db.close()

    try:
        file_bytes = download_file(storage_path)

        ext = filename.lower().rsplit(".", 1)[-1]
        with tempfile.NamedTemporaryFile(suffix=f".{ext}", delete=False) as tmp:
            tmp.write(file_bytes)
            tmp_path = tmp.name

        try:
            text = extract_text(tmp_path, filename)
        finally:
            os.remove(tmp_path)

        chunks = chunk_text(text)
        if not chunks:
            raise ValueError("No extractable text found in file")

        db = SessionLocal()
        vectors = embed_text(chunks)

        for c, vector in zip(chunks, vectors):
            db.add(Chunk(text=c, embedding=vector, document_id=document_id))

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