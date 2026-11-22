from fastapi import FastAPI
from app.database import engine, Base
from app.models import document, user

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def get():
    return {"message": "Notes API"}