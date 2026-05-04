from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session
from src.utills.db import get_db
from src.public import public_controller

publi_routes = APIRouter(prefix="/public")

@publi_routes.get("/products")
def allProduct(db:Session = Depends(get_db)):
    return public_controller.allProducts(db)

@publi_routes.get("/arrivals")
def newArrivalProduct(db:Session = Depends(get_db)):
    return public_controller.allArrivals(db)