from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.admin.models import ProductModel, NewArrivalModel

# === Get Al Products ====
def allProducts(db:Session):
    products = db.query(ProductModel).all()
    return products

def allArrivals(db:Session):
    arrivals = db.query(NewArrivalModel).all()
    return arrivals