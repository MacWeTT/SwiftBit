from database.databaseUtil import db_dependency
from database.dbFuncs import saveToDatabase
from models.models import ShortenedUrl
import uuid, os


def createNewShortenedUrl(
    original_url: str, user_id: int, db: db_dependency
) -> ShortenedUrl:
    """
    Shortens a requested URL.
    """
    identifier = str(uuid.uuid4())[:8]
    shortenedURL = f"{os.environ.get('API_URL')}/{identifier}"

    newShortenedUrl = ShortenedUrl(
        url=original_url,
        short_url=shortenedURL,
        user_id=user_id,
    )
    saveToDatabase(db, newShortenedUrl)

    return newShortenedUrl
