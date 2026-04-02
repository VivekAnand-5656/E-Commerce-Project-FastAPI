from pydantic import BaseModel

class UserSchema(BaseModel):
    name : str
    mobile : str
    email : str
    password : str

class LoginSchema(BaseModel):
    email : str
    password : str