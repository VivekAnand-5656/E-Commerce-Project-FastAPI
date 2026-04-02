from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from src.utills.db import Base

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    mobile = Column(String(10), nullable=False, unique=True)
    email = Column(String(150), nullable=False, unique=True)
    hash_password = Column(String(200), nullable=False, unique=True)
    
    carts = relationship("CartModel", back_populates="user")