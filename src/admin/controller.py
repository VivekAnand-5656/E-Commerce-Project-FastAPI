from src.admin.dtos import ProductSchema, ProductResponse, OrderStatusSchema, NewArrivalProductSchema
from sqlalchemy.orm import Session
from src.admin.models import ProductModel, NewArrivalModel
from fastapi import HTTPException, Request
from src.users.models import UserModel
from src.carts.models import CartModel

# ---- Order Status ------
from src.order.enums import Enum, OrderStatus
from src.order.model import OrderModel 

def create_product_with_image(
    name:str,
    description:str,
    price:int,
    disc_price:int,
    stock:bool,
    catagory:str,
    image_path:str,
    db:Session
):
    new_product = ProductModel(
        name=name,
        description=description,
        price=price,
        disc_price=disc_price,
        stock=stock,
        catagory = catagory,
        image=image_path
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product

# ----- Create New Arrival Product ---------
def create_new_arrival(
    name:str,
    description:str,
    price:int,
    disc_price:int,
    stock:bool,
    catagory:str,
    image_path:str,
    db:Session
):
    new_product = NewArrivalModel(
        name=name,
        description=description,
        price=price,
        disc_price=disc_price,
        stock=stock,
        catagory = catagory,
        image=image_path
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product

# ===== Get All Products ========
def get_all_products(db:Session):
    products = db.query(ProductModel).all()
    return products

# ----- Get all Arrival Products ------
def get_all_new_arrival_products(db:Session):
    products = db.query(NewArrivalModel).all()
    return products
# ======= Get Product By Id =======
def get_one_product(product_id:int,db:Session):
    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not product:
        raise HTTPException(404, detail="Product not found")
    return product
# =========== Clear All Product ========
def clearProducts(db:Session):
    products = db.query(ProductModel).all()
    if not products:
        raise HTTPException(404,detail="Product is Empty")
    db.query(ProductModel).delete()
    db.commit()
    return {"message": "All products deleted successfully"}
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
    orders = db.query(OrderModel).filter(OrderModel.id == body.order_id).first()
    print(orders)
    if not orders:
        raise HTTPException(404, detail="Cart is Empty")
     
    orders.status = body.status
 
    db.commit()
    db.refresh(orders)
    return {
        "status":f"Order ${orders.status}",
        "order id": orders.id,
        "order status" : orders.status
    }