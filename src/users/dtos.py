from pydantic import BaseModel, EmailStr

class UserSchema(BaseModel):
    name : str
    mobile : str
    email : str
    password : str

class LoginSchema(BaseModel):
    email : str
    password : str

class ForgotPasswordSchema(BaseModel):
    email: EmailStr

class ResetPasswordSchema(BaseModel):
    token : str
    newpassword: str

class SearchProductSchema(BaseModel):
    product_name:str

class FilterByCatagorySchema(BaseModel):
    catagory: str