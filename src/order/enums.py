from enum import Enum

class OrderStatus(str,Enum):
    pending = "pending"
    confirmed = "confirmed"
    shipped = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"