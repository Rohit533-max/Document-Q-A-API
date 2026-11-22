from pydantic import BaseModel
from datetime import datetime

class DocumentCreate(BaseModel):
    title: str
    content: str | None = None


class DocumentResponse(BaseModel):
    id : int
    title : str
    content : str | None = None
    created_at : datetime

    model_config = {
        "from_attributes" : True
    }