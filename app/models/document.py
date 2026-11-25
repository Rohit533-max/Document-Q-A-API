from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
from sqlalchemy.sql import func
class Document(Base):
    __tablename__ = "document_table"

    id = Column(Integer, primary_key=True, index= True)
    title = Column(String, nullable= False)
    content = Column(Text, nullable= False)
    created_at = Column(DateTime(timezone=True), server_default= func.now())

    owner_id = Column(Integer, ForeignKey("user_table.id"), nullable=True)
    owner = relationship("User", back_populates="documents")