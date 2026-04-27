import jwt
from datetime import datetime, timedelta
from src.utills.setting import setting

def create_reset_token(user_id:int):
    payload ={
        "_id": user_id,
        "exp": datetime.utcnow() + timedelta(minutes=15)  # 15 min expiry
    }
    return jwt.encode(payload, setting.SECRET_KEY, algorithm=setting.ALGORITHM)