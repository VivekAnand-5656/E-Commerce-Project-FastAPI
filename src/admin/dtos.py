from pydantic import BaseModel
from src.order.enums import OrderStatus

class ProductSchema(BaseModel): 
    name : str
    description : str
    price : int
    disc_price : int
    stock : bool = True
    catagory : str

class NewArrivalProductSchema(BaseModel): 
    name : str
    description : str
    price : int
    disc_price : int
    stock : bool = True
    catagory : str

class ProductResponse(BaseModel): 
    name:str
    description:str
    price:int
    disc_price:int
    stock:bool
    catagory:str
    image:str

   

class OrderStatusSchema(BaseModel):
    status : OrderStatus
    order_id : int