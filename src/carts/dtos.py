from pydantic import BaseModel

class CartSchema(BaseModel):
    user_id : int
    product_id : int
    quantity : int