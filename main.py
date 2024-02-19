from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request, status
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import logging

# Load Environment variables
load_dotenv()

# Used to silence Bcrypt warning log
logging.getLogger("passlib").setLevel(logging.ERROR)

# Router imports
from routes.url import urlRouter
from routes.user import userRouter

# Database functions
from database.connection import engine, Base


apiParams = {
    "debug": True,
    "title": "SwiftBit API",
    "summary": "SwiftBit is a FastAPI powered service that can shorten your urls.",
    "description": "Will be added soon.",
    "version": "0.0.1",
    "openapi_tags": [
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
}


# Application Initialization
Base.metadata.create_all(bind=engine)
app = FastAPI(**apiParams)
app.middleware(CORSMiddleware)


# Router Initialization
app.include_router(urlRouter, tags=["Urls"])
app.include_router(userRouter, tags=["Users"])

# Template and Static File Initialization
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


# Root Route
@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "response": {
                "status": status.HTTP_200_OK,
                "message": "All API services are up and running.",
            },
        },
    )
