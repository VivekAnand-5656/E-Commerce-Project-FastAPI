from enum import Enum

class OrderStatus(str,Enum):
    pending = "pending" 
    shipped = "shipped"
    paid = "paid"
    delivered = "delivered"
    cancelled = "cancelled"