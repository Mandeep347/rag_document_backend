from sqlalchemy import Column, Integer, String, ForeignKey
from pgvector.sqlalchemy import Vector
from app.core.database import Base

class Chunk(Base):
    __tablename__ = "chunks"

    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    text = Column(String, nullable= False)
    embedding = Column(Vector(384))

    