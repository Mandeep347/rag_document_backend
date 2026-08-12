from app.core.database import SessionLocal
from app.models.chunk import Chunk
from app.services.embeddings import embed_text

sentences = [
    "cat sat on a mat",
    "dog ran in the park",
    "stock market crashed today",
]

db = SessionLocal()
for s in sentences:
    vector = embed_text(s)
    db.add(Chunk(text=s, embedding= vector))

db.commit()
db.close()
print("Seeded.")