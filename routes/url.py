from dto.responseDTO import ResponseDTO, ShortenUrlResponseDTO, GetAllShortenedUrlsDTO
from database.databaseUtil import user_dependency, db_dependency, optional_user
from database.dbFuncs import deleteFromDatabase
from fastapi import APIRouter, HTTPException
from models.models import ShortenedUrl
from starlette import status
from typing import Optional
import os


# Services
from services.url import createNewShortenedUrl

urlRouter = APIRouter(prefix="/url")


@urlRouter.get("/")
async def get_user_urls(user: user_dependency, db: db_dependency):
    """
    Fetch all the shortened urls of the user who raised the request.
    """
    try:
        urls = db.query(ShortenedUrl).filter(ShortenedUrl.user_id == user.id).all()
        return [
            GetAllShortenedUrlsDTO(url=url.url, short_url=url.short_url) for url in urls
        ]

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")


@urlRouter.post("/")
async def shorten_new_url(
    db: db_dependency,
    request_url: str,
    user: optional_user,
):
    """
    Accepts a request url and returns a shortened URL.

    The requested URL must be correct otherwise the shortened URL will not work.
    """
    try:
        shortened_url = (
            db.query(ShortenedUrl).filter(ShortenedUrl.url == request_url).first()
        )
        if shortened_url:
            message = "Shortened URL for the requested URL already exists."
        else:
            print(user)
            if user is not None:
                shortened_url = createNewShortenedUrl(db, request_url, user.id)
                message = "Requested URL has been shortened."
            else:
                shortened_url = createNewShortenedUrl(db, request_url, None)
                message = "Requested URL has been shortened."

        return ShortenUrlResponseDTO(
            message=message,
            original_url=request_url,
            shortened_url=shortened_url.short_url,
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")


@urlRouter.delete("/{url_id}")
async def delete_short_url(user: user_dependency, db: db_dependency, url_id: str):
    """
    API Route to delete a user URL.

    Usage: Only enter the ID of the URL (the alphanumeric tag after the root route).

    A url can only be deleted if it belongs to the user who raised the request.
    """
    try:
        requestURL = f"{os.environ.get('API_URL')}/{url_id}"
        urlObject = (
            db.query(ShortenedUrl)
            .filter(ShortenedUrl.short_url == requestURL)
            .filter(ShortenedUrl.user_id == user.id)
            .first()
        )
        deleteFromDatabase(db, urlObject)
        return ResponseDTO(message="Short URL has been deleted successfully.")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")
