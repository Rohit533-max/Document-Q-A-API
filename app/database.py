from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

#local database
DATABASE = "sqlite:///./mydatabase.db"

#engine is the connection to the database
engine = create_engine(DATABASE, connect_args={"check_same_thread":False})

#creating a session
SessionLocal = sessionmaker(autoflush=False, autocommit = False, bind=engine)

class Base(DeclarativeBase):
    pass

#database dependency
def get_db():
    db = SessionLocal()
    try:
        #to provide database session to api endpoint
        yield db
    finally:
        db.close()
        
        