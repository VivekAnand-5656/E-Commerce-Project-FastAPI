from src.admin.dtos import ProductSchema, ProductResponse
from sqlalchemy.orm import Session
from src.admin.models import ProductModel
from fastapi import HTTPException, Request
from src.users.models import UserModel



# ======== Create Product ==========
def create_product(body:ProductSchema,db:Session):
    # data = body.model_dump()
    print(body.model_dump())
    
    new_product = ProductModel(
        name = body.name,
        description = body.description,
        price = body.price,
        disc_price = body.disc_price,
        stock = body.stock
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product

# ===== Get All Products ========
def get_all_products(db:Session):
    products = db.query(ProductModel).all()
    return products
# ======= Get Product By Id =======
def get_one_product(product_id:int,db:Session):
    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not product:
        raise HTTPException(404, detail="Product not found")
    return product
# ======= Delete Product ======
def delete_product(product_id:int, db:Session):
    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not product:
        raise HTTPException(404, detail="Product not found")
    db.delete(product)
    db.commit()

    return {
        "status":"Product Deleted Successfully",
        "product":product
    }

# --------------- Get All User ----------
def all_users(db:Session):
    users = db.query(UserModel).all()
    return users