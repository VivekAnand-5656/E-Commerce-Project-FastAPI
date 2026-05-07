from pydantic import BaseModel
from src.admin.dtos import ProductResponse

class WishlistResponse(BaseModel):
    product : ProductResponse