from app.core.database import SessionLocal
from app.models.chunk import Chunk
from app.models.document import Document
from app.services.embeddings import embed_text
from app.services.pdf_loader import extract_text
from app.services.chunker import chunk_text

pdf_path = "app/scripts/MandeepResumeBackend.pdf"

text = extract_text(pdf_path)
chunks = chunk_text(text)

db = SessionLocal()

doc = Document(filename="MandeepResumeBackend.pdf")
db.add(doc)
db.commit()
db.refresh(doc)
document_id = doc.id

for c in chunks:
    vector = embed_text(c)
    db.add(Chunk(text=c, embedding=vector, document_id= doc.id))
db.commit()
db.close()

print(f"Seeded {len(chunks)} chunks under document_id= {document_id}")