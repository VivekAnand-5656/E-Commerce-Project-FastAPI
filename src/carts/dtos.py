from pydantic import BaseModel
from src.admin.dtos import ProductResponse

 

class CartResponse(BaseModel): 
    product : ProductResponse
