from fastapi import APIRouter, Depends, status, Request, UploadFile, File, Form
from sqlalchemy.orm import Session
from src.utills.db import get_db
from src.admin import controller
from src.admin.dtos import ProductSchema, OrderStatusSchema

# ---- file uploading  
import shutil
import uuid
import os
admin_routes = APIRouter(prefix="/admin")

# -------- File Upload -----
def save_image(file:UploadFile):
    os.makedirs("uploads",exist_ok=True)

    ext = file.filename.split(".")[-1]
    file_name = f"{uuid.uuid4()}.{ext}"
    file_path = f"uploads/{file_name}"

    with open(file_path,"wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return file_path

@admin_routes.get("/")
def welcome():
    return {
        "greet":"Welcome to Admin Page"
    }

# ==== Add Product ====
@admin_routes.post("/addproduct") 
def create_product(
    name: str = Form(...),
    description: str = Form(...),
    price: int = Form(...),
    disc_price: int = Form(...),
    stock: bool = Form(...),
    catagory: str = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    image_path = save_image(image)

    return controller.create_product_with_image(
        name,
        description,
        price,
        disc_price,
        stock,
        catagory,
        image_path,
        db
    )

# ----- Add New Arrival Product ----
@admin_routes.post("/addnewarrivalproduct") 
def create_newarrival_product(
    name: str = Form(...),
    description: str = Form(...),
    price: int = Form(...),
    disc_price: int = Form(...),
    stock: bool = Form(...),
    catagory: str = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    image_path = save_image(image)

    return controller.create_new_arrival(
        name,
        description,
        price,
        disc_price,
        stock,
        catagory,
        image_path,
        db
    )

# ===== Get Products =====
@admin_routes.get("/allproducts")
def allProducts(db:Session = Depends(get_db)):
    return controller.get_all_products(db)
# ---- Get arrival products ------
@admin_routes.get("/newarrivalproducts")
def allnewarrival(db:Session = Depends(get_db)):
    return controller.get_all_new_arrival_products(db)

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

# === Place Order ===
@admin_routes.put("/orderupdate")
def update_order(body:OrderStatusSchema, db:Session=Depends(get_db)):
    return controller.update_order_status(body,db)
 
