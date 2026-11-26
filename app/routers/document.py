from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.document import Document
from app.models.user import User
from app.schemas.document_schema import DocumentCreate, DocumentResponse, DocumentUpdate

router = APIRouter(
    prefix="/document",
    tags=["Document"]
)

@router.get("/", response_model=list[DocumentResponse])
def get_document(db: Session= Depends(get_db)):
    try:
        docs = db.query(Document).all()
        return docs
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong while searching this Document."
        )

@router.post("/{user_id}", response_model=DocumentResponse)
def add_document(user_id : int, docs : DocumentCreate, db: Session = Depends(get_db)):
    db_doc = Document(
        title = docs.title,
        content = docs.content,
        owner_id= user_id
    )
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not Found!"
        )
    try:
        db.add(db_doc)
        db.commit()
        db.refresh(db_doc)
        return db_doc

    except Exception as e:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Something went wrong while creating the document."
        )

@router.get("/{id}", response_model=DocumentResponse)
def get_selected_id(id: int, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == id).first()

    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found!"
        )

    return doc

@router.patch("/{id}", response_model=DocumentResponse)
def edit_document(id: int ,docs: DocumentUpdate, db : Session = Depends(get_db)):
    db_doc = db.query(Document).filter(Document.id == id).first()

    if not db_doc:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail= "User not found"
        )
    try:

        update_data = docs.model_dump(exclude_unset=True)

        for key, val in update_data.items():
            setattr(db_doc, key, val)

        db.commit()
        db.refresh(db_doc)

        return db_doc
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong while updating document."
        ) 

@router.delete("/{id}")
def delete_document(id : int, db: Session = Depends(get_db)):
    db_doc = db.query(Document).filter(Document.id == id).first()

    if not db_doc:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail="Document not found."
        )

    try:
        db.delete(db_doc)
        db.commit()

        return{
            "message": "Document deleted Successfully."
        }
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong."
        )

    