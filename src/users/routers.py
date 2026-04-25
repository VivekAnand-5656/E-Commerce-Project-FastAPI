from fastapi import APIRouter, Depends
from src.utills.db import get_db
from sqlalchemy.orm import Session
from src.users import user_controller
from src.users.dtos import UserSchema, LoginSchema
from src.carts.dtos import CartSchema
from src.users.models import UserModel
from src.utills.helpers import is_login

user_routes = APIRouter(prefix="/users")

@user_routes.post("/create_user")
def create_user(body:UserSchema,db:Session=Depends(get_db)):
    return user_controller.signupUser(body,db)

# --- Login ----
@user_routes.post("/login")
def login(body:LoginSchema, db:Session=Depends(get_db)):
    return user_controller.login(body,db)

# ===== Add to Cart ====
@user_routes.post("/addtocart")
def add_to_cart(body:CartSchema,db:Session = Depends(get_db), user:UserModel = Depends(is_login)):
    return user_controller.add_to_cart(body,db,user)

# ======= Get All Products =====
@user_routes.get("/products")
def all_products(db:Session = Depends(get_db), user:UserModel=Depends(is_login)):
    return user_controller.all_products(db,user)

# --- Get All new arrival -----
@user_routes.get("/allnewarrivalproducts")
def all_new_arrival_product(db:Session=Depends(get_db), user:UserModel= Depends(is_login)):
    return user_controller.get_new_arrival(db,user)
# ===== Order Placed =====
@user_routes.post("/orderplace")
def order(db:Session = Depends(get_db), user:UserModel = Depends(is_login)):
    return user_controller.order_product(db,user)