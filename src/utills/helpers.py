from fastapi import Request, status, HTTPException, Depends
from src.utills.setting import setting
from sqlalchemy.orm import Session
import jwt
from src.users.models import UserModel
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from src.utills.db import get_db

def is_login(request:Request, db:Session=Depends(get_db)):
    try:
        token = request.headers.get("Authorization")
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