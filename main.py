from fastapi import FastAPI 
from src.utills.db import Base, engine
from src.admin.routes import admin_routes
from src.users.routers import user_routes
from fastapi.middleware.cors import CORSMiddleware
# --- Image Uploading ---
from fastapi.staticfiles import StaticFiles

from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup code
    print("Creating Tables....")
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="This is my E-Commerce Project",
    lifespan=lifespan
    )
app.add_middleware(
    CORSMiddleware,  
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Base.metadata.create_all(engine)     for localhost
# --- for Neon  

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup code
    print("Creating Tables....")
    Base.metadata.create_all(bind=engine)
    yield


app.include_router(admin_routes) 
app.include_router(user_routes)

# --- images 
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
