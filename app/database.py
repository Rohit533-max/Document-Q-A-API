from pathlib import Path

from sqlalchemy import create_engine, make_url
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os
from dotenv import load_dotenv
load_dotenv()

#local database
DATABASE = os.getenv("MY_DATABASE")
if not DATABASE:
    raise RuntimeError("MY_DATABASE environment variable is not set")

database_url = make_url(DATABASE)
connect_args = {}
if database_url.get_backend_name() == "sqlite":
    if database_url.database and database_url.database != ":memory:":
        database_path = Path(database_url.database)
        if not database_path.is_absolute():
            database_path = (Path(__file__).resolve().parent / database_path).resolve()
        database_url = database_url.set(
            database=database_path.as_posix()
        )
    connect_args["check_same_thread"] = False

#engine is the connection to the database
engine = create_engine(database_url, connect_args=connect_args)

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
        
        