from sqlalchemy import Column, Integer, String, Boolean 
from sqlalchemy.orm import relationship
from src.utills.db import Base

class ProductModel(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150))
    description = Column(String(250))
    price = Column(Integer)
    disc_price = Column(Integer)
    stock = Column(Boolean)

    carts = relationship("CartModel", back_populates="product")