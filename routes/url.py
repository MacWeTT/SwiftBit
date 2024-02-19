from logging import log
from database.databaseUtil import user_dependency, db_dependency
from dto.responseDTO import ShortenUrlResponseDTO
from models.models import ShortenedUrl
from fastapi import APIRouter
from services.authentication import getCurrentUser


# Services
from services.url import createNewShortenedUrl

urlRouter = APIRouter(prefix="/url")


@urlRouter.get("/")
async def get_user_urls(user: user_dependency, db: db_dependency):
    try:
        urls = db.query(ShortenedUrl).filter(ShortenedUrl.user_id == user["id"]).first()
        return {"urls": urls}
    except Exception as e:
        print(e)
        raise e


@urlRouter.post("/")
async def shorten_new_url(user: user_dependency, db: db_dependency, request_url: str):
    try:
        shortened_url = (
            db.query(ShortenedUrl).filter(ShortenedUrl.url == request_url).first()
        )
        # current_user = getCurrentUser(user)
        if shortened_url:
            message = "Shortened URL for the requested URL already exists."
        else:
            shortened_url = createNewShortenedUrl(request_url, db)
            message = "Requested URl has been shortened."

        return ShortenUrlResponseDTO(
            message=message,
            original_url=request_url,
            shortened_url=shortened_url,
        )
    except Exception as e:
        print(e)
        raise e
