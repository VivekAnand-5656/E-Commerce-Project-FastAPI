from src.users.dtos import UserSchema, LoginSchema, ForgotPasswordSchema, ResetPasswordSchema, SearchProductSchema, FilterByCatagorySchema
from src.admin.dtos import ProductSchema
from sqlalchemy.orm import Session
from src.users.models import UserModel
from src.admin.models import NewArrivalModel
from fastapi import HTTPException, status, Request, Depends
from src.utills.db import get_db
from pwdlib import PasswordHash
from src.utills.setting import setting
from datetime import datetime,timedelta, timezone
import jwt
from jwt.exceptions import InvalidTokenError,ExpiredSignatureError
from sqlalchemy import func 
from src.carts.models import CartModel

from src.admin.models import ProductModel
# ===== Order Model ==== 
from src.order.dtos import OrderSchema
from src.order.enums import Enum, OrderStatus
from src.order.model import OrderModel, OrderItem

# ========= Forgot Password ============
from src.users.resettoken import create_reset_token


password_hash = PasswordHash.recommended()

def get_password_hash(password):
    return password_hash.hash(password)

def verify_password(plain_password,hashed_password):
    return password_hash.verify(plain_password,hashed_password)

# =============== Signup ===========
def signupUser(body:UserSchema, db:Session):
    print("Body: ",body)
    exist_email = db.query(UserModel).filter(
        UserModel.email == body.email
    ).first()

    esist_mobile = db.query(UserModel).filter(
        UserModel.mobile == body.mobile
    ).first()

    if exist_email:
        raise HTTPException(400, detail="Email already exist")
    
    if esist_mobile:
        raise HTTPException(400, detail="Mobile Number already exist")
    hashed_pwd = get_password_hash(body.password)
    new_user = UserModel(
        name = body.name,
        mobile = body.mobile,
        email = body.email,
        hash_password = hashed_pwd
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# ========== Login User ============
def login(body:LoginSchema, db:Session):
    user = db.query(UserModel).filter(UserModel.email == body.email).first()
    if not user:
        raise HTTPException(401, detail="Unauthorized User")
    userpassword = db.query(UserModel).filter(UserModel.hash_password == body.password).first()
    if not verify_password(body.password, user.hash_password):
        raise HTTPException(401, detail="Unauthorized User")
    exp_time = datetime.now()+timedelta(minutes=setting.EXP_TIME)
    payload ={
        "_id":user.id,
        "exp":exp_time
    }
    token = jwt.encode(
        payload,
        setting.SECRET_KEY,
        setting.ALGORITHM
    )

    return {
        "id":user.id,
        "token": token
    }

# ------- Token Send --------
# =========== Add To Cart ==========
def add_to_cart(productid:int,db:Session, user): 
    product = db.query(ProductModel).filter(ProductModel.id == productid).first()
    if not product:
        raise HTTPException(404, detail="Product not found")
    # === Testing ====
    cart_item = db.query(CartModel).filter(CartModel.user_id == user.id, CartModel.product_id == productid ).first()
     
    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = CartModel(
            user_id = user.id,
            product_id = productid,
            quantity = 1,
            carttotal = product.price
        )
        db.add(cart_item)
    db.commit()
    db.refresh(cart_item)

    return  product 

# ======= Increase Quantity of Cart ==========
def update_quantity(productid:int,db:Session,user): 
    cartitem = db.query(CartModel).filter(CartModel.user_id == user.id, CartModel.product_id == productid).first()
    if not cartitem:
        raise HTTPException(404, detail="Product not in Cart")
    
    cartitem.quantity += 1
    cartitem.carttotal = cartitem.quantity * cartitem.product.price
    db.commit()
    db.refresh(cartitem)

    return {
        "status":"Quantity Updated",
        "quantity":cartitem.quantity,
        "totalcartprice" : cartitem.carttotal
    }
# ======= Decrease Quantity of Cart ==========
def decrease_quantity(productid:int,db:Session,user): 
    cartitem = db.query(CartModel).filter(CartModel.user_id == user.id, CartModel.product_id == productid).first()
    if not cartitem:
        raise HTTPException(404, detail="Product not in Cart")
    
    cartitem.quantity -= 1
    cartitem.carttotal = cartitem.carttotal - cartitem.product.price
    if cartitem.quantity == 0:
        db.delete(cartitem)
        db.commit()
        return {
            "msg":"Product Removed from Cart"
        }
    db.commit()
    db.refresh(cartitem)

    return {
        "status":"Quantity Updated",
        "quantity":cartitem.quantity,
        "Cart Total":cartitem.carttotal
    }

# ========= Get User Cart ======
def get_user_cart(db:Session,user):
    carts = db.query(CartModel).all()
    
    for pr in carts:
        print("Cart Product:- ",pr.product)
    if len(carts) == 0:
        raise HTTPException(404, detail="Cart is Empty")
    return carts

# ======= Remove From Cart ======
def remove_item_cart(cartId:int,db:Session,user):
    cart = db.query(CartModel).filter(CartModel.id == cartId).first()
    if not cart:
        raise HTTPException(404, detail="Cart not found")
    db.delete(cart)
    db.commit()

    return {
        "status":"Cart Removed",
        "cart": cart
    }

# ====== Clear All Cart ========
def clear_cart(db:Session,user):
    carts = db.query(CartModel).filter(CartModel.user_id == user.id)

    if not carts.first():
        raise HTTPException(404, detail="Cart is Empty")
    
    carts.delete(synchronize_session=False)
    db.commit()
    return {
        "status":"Cart Cleared"
    }

# ==== Token Send ====
def is_login(request:Request, db:Session=Depends(get_db)):
    try:
        token = request.headers.get("Authorizatoni")
        if not token:
            raise HTTPException(401, detail="Authorization headers missing")
        token = token.split(" ")[-1]
        data = jwt.decode(token, setting.SECRET_KEY, setting.ALGORITHM)
        user_id = data.get("_id")
        if user_id is None:
            raise HTTPException(401, detail="Please Login First")
        user = db.query(UserModel).filter(UserModel.id == user_id).first()

        if not user:
            raise HTTPException(401, detail="Login Please")
        print(data)
        return user
    except ExpiredSignatureError:
        raise HTTPException(401, detail="Token Expired")
    except InvalidTokenError:
        raise HTTPException(401, detail="Invalid Toen")
    
# ======== Get Products =======
def all_products(db:Session, user):
    products = db.query(ProductModel).all()
    return products
# ---- Get new arrival products ----
def get_new_arrival(db:Session,user):
    products = db.query(NewArrivalModel).all()
    return products
# ======== Order Placed ======
# ===== This is Incomplete =====================================================================
def order_product(db:Session,user):
    cart_items = db.query(CartModel).filter(CartModel.user_id == user.id).all()
    print(cart_items)
    if not cart_items:
        raise HTTPException(400, detail="Cart is Empty")
    total = 0
    products = []
    for item in cart_items:
        product = db.query(ProductModel).filter(ProductModel.id == item.product_id).first()
        products.append(product)
        total += item.carttotal
        

    print("Total Price:- ",total)
    new_order = OrderModel(
        user_id = user.id,
        total_price = total,
        status = OrderStatus.pending
    )
    print("Order Placed Successfully ✅")

    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    # ---------- Add order items -------
    for item in cart_items:
        product = db.query(ProductModel).filter(ProductModel.id == item.product_id ).first()
        total += item.carttotal
        order_item = OrderItem(
            order_id = new_order.id,
            product_id = item.product_id,
            quantity = item.quantity,
            price = product.price
        )
        db.add(order_item)
    new_order.total_price = total
# ---------- Delete Cart Items -------
    for item in cart_items:
        db.delete(item)

    db.commit()

    return {
        "status":"Order Placed Succesfylly",
        "Total ":total,
        "New Order Id: ": new_order.id
    }

# ============== Get My Orders ==============
def get_my_orders(db: Session, user):

    orders = db.query(OrderModel).filter(OrderModel.user_id == user.id).all()

    result = []

    for order in orders:
        items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()

        order_data = {
            "order_id": order.id,
            "total_price": order.total_price,
            "status": order.status,
            "items": []
        }

        for item in items:
            product = db.query(ProductModel).filter(ProductModel.id == item.product_id).first()
            
            order_data["items"].append({
                "product": {
                    "id": product.id,
                    "image":product.image,
                    "name": product.name,
                    "price": product.price,
                    "description": product.description
                },
                "quantity": item.quantity
            })

        result.append(order_data)

    return result
# -------------- Forgot Password --------------
def forgot_password(body:ForgotPasswordSchema,db:Session):
    user = db.query(UserModel).filter(UserModel.email == body.email).first()
    if not user:
        raise HTTPException(404, "User with this email not found")
    reset_token = create_reset_token(user.id)
    return {
        "msg": "Password reset token generated",
        "reset_token": reset_token
    }

# ---- Reset Password ----
def reset_password(body:ResetPasswordSchema,db:Session):
    try:
        payload = jwt.decode(body.token, setting.SECRET_KEY, algorithms=[setting.ALGORITHM])
        user_id = payload.get("_id")
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            raise HTTPException(404, "User not found")
        
        hashed_password = get_password_hash(body.newpassword)
        user.hash_password = hashed_password
        db.commit()
        return {"msg": "Password reset successful"}
    except ExpiredSignatureError:
        raise HTTPException(400, "Reset token expired")

    except InvalidTokenError:
        raise HTTPException(400, "Invalid reset token")

# ------ Get User Profile -------
def get_user_profile(current_user):
    return {
        "id":current_user.id,
        "name":current_user.name,
        "email": current_user.email
    }

# ========= Search Products ========
def search_products(body:SearchProductSchema,db:Session): 
    product = (db.query(ProductModel).filter(ProductModel.name.ilike(f"%{body.product_name}%")).all()) 
    return product

# ======= Filter By Catagory ======
def filter_by_catagory(body:FilterByCatagorySchema,db:Session):
    products = (db.query(ProductModel).filter(ProductModel.catagory.ilike(f"%{body.catagory}%")).all())
    return products

