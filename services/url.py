from database.databaseUtil import db_dependency
from database.dbFuncs import saveToDatabase
from models.models import ShortenedUrl
import uuid, os

from services.authentication import getCurrentUser


def createNewShortenedUrl(
    original_url: str, user_id: int, db: db_dependency
) -> ShortenedUrl:

    identifier = str(uuid.uuid4())[:8]
    baseURL = os.environ.get("API_URL")
    shortenedURL = f"{baseURL}/{identifier}"

    newShortenedUrl = ShortenedUrl(
        url=original_url,
        short_url=shortenedURL,
        user_id=user_id,
    )
    saveToDatabase(db, newShortenedUrl)

    return newShortenedUrl
