from sqlalchemy import Column, Integer , ForeignKey, Enum as SqlEnum
from src.utills.db import Base
from src.order.enums import OrderStatus
from sqlalchemy.orm import relationship

class OrderModel(Base):
    __tablename__ = "orders"

    id = Column(Integer,primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    total_price = Column(Integer)
    status = Column(SqlEnum(OrderStatus), default=OrderStatus.pending)

    user = relationship("UserModel", back_populates="orders")
    items = relationship("OrderItem",back_populates="order",cascade="all, delete")

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer,primary_key=True, index=True)
    
    order_id = Column(Integer,ForeignKey("orders.id"))
    product_id = Column(Integer,ForeignKey("products.id"))
    quantity = Column(Integer,default=1)
    price = Column(Integer)

    order = relationship("OrderModel",back_populates="items")
    product = relationship("ProductModel",)