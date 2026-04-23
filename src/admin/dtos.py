from pydantic import BaseModel
from src.order.enums import OrderStatus

class ProductSchema(BaseModel): 
    name : str
    description : str
    price : int
    disc_price : int
    stock : bool = True
    catagory : str

class ProductResponse(BaseModel):
    id : int
    name : str
    description : str
    price : int
    disc_price : int
    stock : bool = True

class OrderStatusSchema(BaseModel):
    status : OrderStatus
    user_id : int