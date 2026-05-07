from sqlalchemy import Column, Integer, String, ForeignKey
from src.utills.db import Base
from sqlalchemy.orm import relationship

class WishlistModel(Base):
    __tablename__ = "wishlist"

    id =  Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id") )
    product_id = Column(Integer, ForeignKey("products.id") )

    # -------- relationship---------
    user = relationship("UserModel", back_populates="wishlist" )
    product = relationship("ProductModel", back_populates="wishlist")