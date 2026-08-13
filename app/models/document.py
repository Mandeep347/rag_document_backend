from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    filename = Column(String, nullable= False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)