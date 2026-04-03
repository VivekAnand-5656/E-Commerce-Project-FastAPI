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