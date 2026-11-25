from fastapi import FastAPI
from app.database import engine, Base
from app.models import document, user
from app.routers.user import router as user_router
from app.routers.document import router as document_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_router)
app.include_router(document_router)
@app.get("/")
def get():
    return {"message": "Notes API"}
