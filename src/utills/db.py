from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.utills.setting import setting

Base = declarative_base()
engine = create_engine(url=setting.DB_CONNECTION)
LocalSession = sessionmaker(bind=engine)

def get_db():
    session = LocalSession()
    try:
        yield session
    finally:
        session.close()
        