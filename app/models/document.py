from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index= True)
    title = Column(String, nullable= False)
    content = Column(Text, nullable= False)

    owner_id = Column(Integer, ForeignKey("user_table.id"), nullable=False)
    owner = relationship("User", back_populates="documents")