from pydantic import BaseModel

class CartSchema(BaseModel): 
    product_id : int
    quantity : int