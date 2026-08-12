from app.core.database import Base, engine
from app.models.chunk import Chunk
from app.models.document import Document

Base.metadata.create_all(bind=engine)
print("Tables created.")