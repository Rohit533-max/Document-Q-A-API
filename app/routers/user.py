from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user_schemas import UserCreate, UserResponse

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
        name = User.username,
        email = User.email,
        password = user.password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

@router.get("/{id}", response_model=UserResponse)
def get_selected_user(id : int, db : Session = Depends(get_db)):

    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not Found!"
        )
    return user
