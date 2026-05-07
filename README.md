🛒 E-Commerce Backend API

This project is the backend service for a full-stack E-Commerce web application built using FastAPI.
It provides a complete REST API for user authentication, product browsing, cart management, wishlist handling and order placement.

The aim of this project was to design a clean and modular backend that can easily connect with any frontend (React) and handle real-world e-commerce workflows.

⚙️ Tech Stack
Language: Python
Framework: FastAPI
Authentication: JWT Token Based Auth
Database Migration: Alembic
Database: PostgreSQL
Server: Uvicorn
Project Structure: Modular architecture
📁 Project Structure
backend/
│
├── alembic/            Database migrations
├── src/
│   ├── admin/          Admin APIs
│   ├── carts/          Cart management
│   ├── config/         App configuration
│   ├── order/          Order management
│   ├── public/         Public product APIs
│   ├── users/          Authentication & profile
│   ├── utils/          Helper functions
│   └── wishlist/       Wishlist management
│
├── uploads/            Uploaded product images
├── main.py             Application entry point
├── requirements.txt    Dependencies
├── alembic.ini         Alembic configuration
└── Procfile            Deployment config
🔐 Authentication

The API uses JWT based authentication.
After login, protected routes require an access token in the request header:

Authorization: Bearer <token>
👤 Users API
Authentication

POST /users/create_user
Register a new user account.

POST /users/login
Login user and return access token.

POST /users/forgot-password
Send password reset OTP / link.

POST /users/reset-password
Reset user password using OTP/token.

Profile

GET /users/my-profile
Fetch details of the logged-in user.

🛍️ Products (User Side)

GET /users/products
Fetch all available products.

GET /users/allnewarrivalproducts
Fetch newly added products.

POST /users/search
Search products by keyword.

POST /users/filterbycatagory
Filter products by category.

🛒 Cart APIs

POST /users/addtocart/{productid}
Add a product to cart.

PATCH /users/updatequantity/{productid}
Increase or update product quantity.

PATCH /users/decreasequantity/{productid}
Decrease product quantity.

GET /users/user-cart
Fetch all items in user cart.

DELETE /users/removecart/{cartId}
Remove a single item from cart.

DELETE /users/clearcart
Remove all items from cart.

❤️ Wishlist APIs

POST /users/addtowishlist/{productid}
Add product to wishlist.

GET /users/getwishlists
Fetch wishlist items.

DELETE /users/removewishlist/{wishlistid}
Remove item from wishlist.

📦 Order APIs

POST /users/orderplace
Place a new order from cart.

GET /users/myorders
Fetch all orders of logged-in user.

✨ Key Features
JWT authentication system
Password reset flow
Product search and category filtering
Full cart management system
Wishlist functionality
Order placement workflow
Clean modular folder structure
▶️ Running the Project

Clone the repository and install dependencies:

pip install -r requirements.txt

Start the development server:

uvicorn main:app --reload

The API will be available at:

https://e-commerce-project-3365.onrender.com