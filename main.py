from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from models.models import ShortenedUrl
from dotenv import load_dotenv
import logging, os

# Load Environment variables
load_dotenv()

# Used to silence Bcrypt warning log
logging.getLogger("passlib").setLevel(logging.ERROR)

# Router imports
from routes.url import urlRouter
from routes.user import userRouter

# Database functions
from database.connection import engine, Base
from database.databaseUtil import db_dependency


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


# Service Route
@app.get("/{url}")
async def getUrl(url: str, db: db_dependency):
    """
    This is the core URL of the application.

    Usage: 'http://localhost:8000/{x}'

    Here, x is the unique UUID of your URL that has been shortened by the server.

    If the URL is correct, you will be redirected correctly to your requested URL.
    """

    try:
        requestedURL = f"{os.environ.get('API_URL')}/{url}"
        fullURL = (
            db.query(ShortenedUrl)
            .filter(ShortenedUrl.short_url == requestedURL)
            .first()
            .url
        )
        if not fullURL:
            raise HTTPException(status_code=404, detail="URL Not Found")

        return RedirectResponse(url=f"{fullURL}", status_code=status.HTTP_302_FOUND)
    except Exception as e:
        print(e)
        raise e
