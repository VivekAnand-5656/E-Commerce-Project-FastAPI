from src.admin.dtos import ProductSchema, ProductResponse, OrderStatusSchema
from sqlalchemy.orm import Session
from src.admin.models import ProductModel
from fastapi import HTTPException, Request
from src.users.models import UserModel

# ---- Order Status ------
from src.order.enums import Enum, OrderStatus
from src.order.model import OrderModel 


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

# ======= Update Order Status ========
def update_order_status(body:OrderStatusSchema,db:Session):
    orders = db.query(OrderModel).filter(OrderModel.user_id == body.user_id).first()
    print(orders)
    if not orders:
        raise HTTPException(404, detail="Orders Empty")
     
    orders.status = body.status
 
    db.commit()
    db.refresh(orders)
    return {
        "status":" Order Shipped",
        "order id": orders.id,
        "order status" : orders.status
    }