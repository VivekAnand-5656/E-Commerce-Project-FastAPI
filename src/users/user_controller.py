from src.users.dtos import UserSchema, LoginSchema
from sqlalchemy.orm import Session
from src.users.models import UserModel
from fastapi import HTTPException, status, Request, Depends
from src.utills.db import get_db
from pwdlib import PasswordHash
from src.utills.setting import setting
from datetime import datetime,timedelta, timezone
import jwt
from jwt.exceptions import InvalidTokenError,ExpiredSignatureError

from src.carts.dtos import CartSchema
from src.carts.models import CartModel

from src.admin.models import ProductModel
# ===== Order Model ====
from src.order.model import OrderModel
from src.order.dtos import OrderSchema
from src.order.enums import Enum, OrderStatus

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
def add_to_cart(body:CartSchema,db:Session, user):
    print(body.model_dump())
    cart = CartModel(
        user_id = user.id,
        product_id = body.product_id,
        quantity = body.quantity
    )
    db.add(cart)
    db.commit()
    db.refresh(cart)

    return {
        "status":"Product added to Cart Successfully",
        "cart":cart
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

# ======== Order Placed ======
def order_product(db:Session,user):
    cart_items = db.query(CartModel).filter(CartModel.user_id == user.id).all()
    print(cart_items)
    if not cart_items:
        raise HTTPException(400, detail="Cart is Empty")
    total = 0
    for item in cart_items:
        product = db.query(ProductModel).filter(ProductModel.id == item.product_id).first()
        total += product.disc_price * item.quantity

    print("Total Price:- ",total)
    new_order = OrderModel(
        user_id = user.id,
        total_price = total,
        status = OrderStatus.pending
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    for item in cart_items:
        db.delete(item)

    db.commit()

    return {
        "status":"Order Placed Succesfylly",
        "order":new_order
    }
