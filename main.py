from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import logging, os

# Load Environment variables
load_dotenv()

# Used to silence Bcrypt warning log
logging.getLogger("passlib").setLevel(logging.ERROR)

# Router imports
from routes.root import rootRouter
from routes.url import urlRouter
from routes.user import userRouter

# Database functions
from database.connection import engine, Base
from database.databaseUtil import db_dependency


apiParams = {
    "debug": os.environ.get("DEBUG", False),
    "title": "SwiftBit API",
    "summary": "SwiftBit is a FastAPI powered service that can shorten your urls.",
    "version": "1.0.1",
    "openapi_tags": [
        {
            "name": "Root",
            "description": "Root operations. Check health or input shortened URL to redirect.",
        },
        {
            "name": "Users",
            "description": "User level operations.",
        },
        {
            "name": "Urls",
            "description": "Create and manage short URLs.",
        },
    ],
    "contact": {
        "name": "MacWeTT",
        "url": "https://github.com/MacWeTT",
        "email": "manasbajpai18@gmail.com",
    },
    "license_info": {
        "name": "MIT License",
        "url": "https://github.com/MacWeTT/SwiftBit/blob/main/LICENSE.txt",
    },
    "swagger_ui_parameters": {"defaultModelsExpandDepth": -1},
}


# Application Initialization
Base.metadata.create_all(bind=engine)
app = FastAPI(**apiParams)
app.middleware(CORSMiddleware)


# Router Initialization
app.include_router(rootRouter, tags=["Root"])
app.include_router(urlRouter, tags=["Urls"])
app.include_router(userRouter, tags=["Users"])
