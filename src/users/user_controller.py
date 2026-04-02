from src.users.dtos import UserSchema, LoginSchema
from sqlalchemy.orm import Session
from src.users.models import UserModel
from fastapi import HTTPException, status, Request
from pwdlib import PasswordHash
from src.utills.setting import setting
from datetime import datetime,timedelta, timezone
import jwt
from jwt.exceptions import InvalidTokenError,ExpiredSignatureError

from src.carts.dtos import CartSchema
from src.carts.models import CartModel

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
        setting.SECRET_KEY,
        setting.ALGORITHM
    )

    return {
        "id":user.id,
        "token": token
    }

# ------- Token Send --------
# =========== Add To Cart ==========
def add_to_cart(body:CartSchema,db:Session):
    print(body.model_dump())
    cart = CartModel(
        user_id = body.user_id,
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