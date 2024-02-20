from fastapi import APIRouter, HTTPException, status
from database.databaseUtil import db_dependency
from fastapi.responses import RedirectResponse
from dto.responseDTO import ResponseDTO
from models.models import ShortenedUrl
import os

rootRouter = APIRouter()


# Root Route
@rootRouter.get("/")
async def root():
    """
    Root URL of the application.

    Can be sent a GET request to check whether the service is working or not.
    """
    return ResponseDTO(message="All API services are up and running.")


# Service Route
@rootRouter.get("/{url}")
async def getUrl(url: str, db: db_dependency):
    """
    This is the core URL of the application.

    Usage: 'http://localhost:8000/{x}'

    Here, x is the unique UUID of your URL that has been shortened by the server.

    If the URL is correct, you will be redirected correctly to your requested URL.

    Note: Input the URL in your browser tab, otherwise the redirection won't work.
    """

    try:
        requestedURL = f"{os.environ.get('API_URL')}/{url}"
        fullURL = (
            db.query(ShortenedUrl)
            .filter(ShortenedUrl.short_url == requestedURL)
            .first()
            .url
        )
        return RedirectResponse(url=f"{fullURL}", status_code=status.HTTP_302_FOUND)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="URL Not Found. Make sure the request URL is correct and try again.",
        )
