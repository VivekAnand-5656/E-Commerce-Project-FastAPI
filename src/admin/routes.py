from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session
from src.utills.db import get_db
from src.admin import controller
from src.admin.dtos import ProductSchema
# ---------- users ----- 

admin_routes = APIRouter(prefix="/admin")

@admin_routes.get("/")
def welcome():
    return {
        "greet":"Welcome to Admin Page"
    }

# ==== Add Product ====
@admin_routes.post("/addproduct")
def create_product(body:ProductSchema, db:Session = Depends(get_db)):
    # print(body.id)
    return controller.create_product(body,db)

# ===== Get Products =====
@admin_routes.get("/allproducts")
def allProducts(db:Session = Depends(get_db)):
    return controller.get_all_products(db)

@admin_routes.get("/getproductById/{product_id}")
def get_one_product(product_id:int , db:Session = Depends(get_db)):
    return controller.get_one_product(product_id,db)

# ======== Delete Product =======
@admin_routes.delete("/delete_product/{product_id}")
def delete_product(product_id:int, db:Session = Depends(get_db)):
    return controller.delete_product(product_id,db)

# ======================= Users ==============

# ------- See All Users ---------
@admin_routes.get("/allUser")
def all_users(db:Session=Depends(get_db)):
    return controller.all_users(db)
