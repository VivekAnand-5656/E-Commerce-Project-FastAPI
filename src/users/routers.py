from fastapi import APIRouter, Depends
from src.utills.db import get_db
from sqlalchemy.orm import Session
from src.users import user_controller
from src.users.dtos import UserSchema, LoginSchema, ForgotPasswordSchema, ResetPasswordSchema, SearchProductSchema, FilterByCatagorySchema
from src.carts.dtos import CartResponse
from src.users.models import UserModel
from src.utills.helpers import is_login 
from src.admin.dtos import ProductResponse

user_routes = APIRouter(prefix="/users")

@user_routes.post("/create_user")
def create_user(body:UserSchema,db:Session=Depends(get_db)):
    return user_controller.signupUser(body,db)

# --- Login ----
@user_routes.post("/login")
def login(body:LoginSchema, db:Session=Depends(get_db)):
    return user_controller.login(body,db)

# ===== Add to Cart ====
@user_routes.post("/addtocart/{productid}", response_model=ProductResponse)
def add_to_cart(productid:int,db:Session = Depends(get_db), user:UserModel = Depends(is_login)):
    return user_controller.add_to_cart(productid,db,user)
# ====== Increase Quantity of Cart ======
@user_routes.patch("/updatequantity/{productid}")
def updatequantitycart(productid:int,db:Session = Depends(get_db), user:UserModel = Depends(is_login)):
    return user_controller.update_quantity(productid,db,user)
# ====== Decrease Quantity of Cart ======
@user_routes.patch("/decreasequantity/{productid}")
def updatequantitycart(productid:int,db:Session = Depends(get_db), user:UserModel = Depends(is_login)):
    return user_controller.decrease_quantity(productid,db,user)

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

# ====== Forgot Password ======
@user_routes.post("/forgot-password")
def forgotPassword(body:ForgotPasswordSchema,db:Session= Depends(get_db)):
    return user_controller.forgot_password(body,db)

@user_routes.post("/reset-password")
def resetPassword(body:ResetPasswordSchema, db:Session = Depends(get_db)):
    return user_controller.reset_password(body,db)

# ==== Get User Profile ====
@user_routes.get("/my-profile")
def get_my_profile(current_user=Depends(is_login)):
    return user_controller.get_user_profile(current_user)

# ==== Search Products ====
@user_routes.post("/search")
def search_product(body:SearchProductSchema,db:Session=Depends(get_db)):
    return user_controller.search_products(body,db)

# ====== Filter By Catagoryes =====
@user_routes.post("/filterbycatagory")
def filter_catagory(body:FilterByCatagorySchema,db:Session = Depends(get_db)):
    return user_controller.filter_by_catagory(body,db)

# === Get User Cart ====
@user_routes.get("/user-cart")
def user_cart(db:Session = Depends(get_db),user:UserModel = Depends(is_login)):
    return user_controller.get_user_cart(db,user)

# ==== Remove Cart ====
@user_routes.delete("/removecart/{cartId}")
def remove_cart(cartId:int,db:Session = Depends(get_db),user:UserModel = Depends(is_login)):
    return user_controller.remove_item_cart(cartId,db,user)

# ======== Clear Cart ====
@user_routes.delete("/clearcart")
def clear_carts(db:Session = Depends(get_db),user:UserModel= Depends(is_login)):
    return user_controller.clear_cart(db,user)