from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.utills.setting import setting
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()
# engine = create_engine(url=setting.DB_CONNECTION)
# LocalSession = sessionmaker(bind=engine)

#     for Neon DB 
engine = create_engine(
    setting.DB_CONNECTION,
    pool_pre_ping=True,
    pool_recycle=300
)

LocalSession = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    session = LocalSession()
    try:
        yield session
    finally:
        session.close()
        