from fastapi import FastAPI
from app.routers.user import router as user_router
from app.routers.document import router as document_router

app = FastAPI()

app.include_router(user_router)
app.include_router(document_router)
@app.get("/")
def get():
    return {"message": "Notes API"}
