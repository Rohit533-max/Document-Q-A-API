from  fastapi import FastAPI
app = FastAPI()

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


@app.put("/{idx}")
def put_val(idx:int):
    for note in notes:
        if note["id"] == idx:
            note["title"] = input("string")
            note["content"] = input("string")


    
