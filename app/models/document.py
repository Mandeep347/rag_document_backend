from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from datetime import datetime
from app.core.database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    filename = Column(String, nullable= False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String, default="processing")
    error_message = Column(String, nullable=True)
    created_at = Column(DateTime, server_default= func.now())