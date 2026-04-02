from pydantic import BaseModel

class ProductSchema(BaseModel):
    name : str
    description : str
    price : int
    disc_price : int
    stock : bool = True

class ProductResponse(BaseModel):
    id : int
    name : str
    description : str
    price : int
    disc_price : int
    stock : bool = True