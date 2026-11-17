from  fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
app = FastAPI()

class Note(BaseModel):
    title:str | None = None
    content:str | None = None

notes = [
    {
        "id":1,
        "title":"FastAPI",
        "content": "FastAPI is a Python Framework for building API's"
    },
    {
        "id": 2,
        "title": "Learning Python",
        "content": "Python supports object-oriented programming."
    },
    {
        "id": 3,
        "title": "Learning RAG",
        "content": "RAG combines retrieval with language generation."
    }

]

# route
@app.get("/")
def get_list():
    return notes

# get by an id 
@app.get("/notes/{id}")
def get_by_id(id:int):
    for node in notes:
        if node["id"] == id:
            return node
    return "Invalid Value!"


#put 
@app.put("/put/{id}")
def update_note(id:int, note:Note):
    for data in notes:
        if data["id"] == id:
            data["title"] = note.title
            data["content"] = note.content
            return data

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

#patch
@app.patch("/patch/{id}")
def update_note(id:int, note:Note):
    for data in notes:
        if data["id"] == id:
            if note.title is not None:
                data["title"] = note.title

            if note.content is not None:
                data["content"] = note.content

            return data

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@app.delete("/delete/{id}")
def delete_note(id: int):
    for data in notes:
        if data["id"] == id:
            notes.remove(data)

            return "Deleted successful"
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)