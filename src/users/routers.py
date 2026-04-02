from fastapi import APIRouter, Depends
from src.utills.db import get_db
from sqlalchemy.orm import Session
from src.users import user_controller
from src.users.dtos import UserSchema, LoginSchema
from src.carts.dtos import CartSchema

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
def add_to_cart(body:CartSchema,db:Session = Depends(get_db)):
    return user_controller.add_to_cart(body,db)