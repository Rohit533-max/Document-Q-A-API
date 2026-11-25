from pydantic import BaseModel
from datetime import datetime

class DocumentCreate(BaseModel):
    title: str
    content: str 


class DocumentResponse(BaseModel):
    id : int
    title : str
    content : str 
    created_at : datetime

    model_config = {
        "from_attributes" : True
    }

class DocumentUpdate(BaseModel):
    title : str | None = None
    content : str | None = None
    