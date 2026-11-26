from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user_schemas import UserCreate, UserResponse, UpdateUser
from app.schemas.document_schema import DocumentResponse

router = APIRouter(
    prefix="/users",
    tags=["User"]
)

@router.get("/", response_model=list[UserResponse])
def get_user(db: Session = Depends(get_db)):

    try:
        users = db.query(User).all()
        return users
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong while searching users."
        )

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate,db: Session = Depends(get_db)):
    db_user = User(
        name = user.name,
        email = user.email,
        password = user.password
    )
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Something went wrong while creating the document."
        )

@router.get("/{id}", response_model=UserResponse)
def get_selected_user(id : int, db : Session = Depends(get_db)):

    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not Found!"
        )
    return user

@router.patch("/{id}", response_model=UserResponse)
def edit_user(id: int, user: UpdateUser, db : Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == id).first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    try:
        update_data = user.model_dump(exclude_unset=True)

        for key, val in update_data.items():
            setattr(db_user, key, val)

        db.commit()
        db.refresh(db_user)

        return db_user
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong while updating User."
        )

@router.get("/{user_id}/documents", response_model= list[DocumentResponse])
def get_userdocuments(user_id:int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    return user.documents


@router.delete("/{id}")
def delete_user(id : int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == id).first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not Found"
        )
    try:
        db.delete(db_user)
        db.commit()

        return{
            "message":"User Deleted Successfully."
        }
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong."
        )
    