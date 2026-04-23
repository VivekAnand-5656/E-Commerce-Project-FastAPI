from fastapi import FastAPI 
from src.utills.db import Base, engine
from src.admin.routes import admin_routes
from src.users.routers import user_routes
# --- Image Uploading ---
from fastapi.staticfiles import StaticFiles


app = FastAPI(title="This is my E-Commerce Project")
Base.metadata.create_all(engine)

app.include_router(admin_routes) 
app.include_router(user_routes)

# --- images 
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
