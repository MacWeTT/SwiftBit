from fastapi import FastAPI, Request, openapi, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import logging

# Used to silence Bcrypt warning log
logging.getLogger("passlib").setLevel(logging.ERROR)

# Router imports
from routes.url import urlRouter
from routes.user import userRouter

# Database functions
from database.connection import engine, Base

Base.metadata.create_all(bind=engine)

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
    "license_info": {},
}


# Application Initialization
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
