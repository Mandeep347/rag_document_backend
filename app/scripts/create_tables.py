from app.core.database import Base, engine
from app.models import User, Document, Chunk

Base.metadata.create_all(bind=engine)
print("Tables created.")