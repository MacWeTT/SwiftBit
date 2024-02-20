from database.databaseUtil import db_dependency
from database.dbFuncs import saveToDatabase
from models.models import ShortenedUrl
import uuid, os


def createNewShortenedUrl(
    db: db_dependency, original_url: str, user_id: int | None
) -> ShortenedUrl:
    """
    Shortens a requested URL.
    """
    identifier = str(uuid.uuid4())[:8]
    shortenedURL = f"{os.environ.get('API_URL')}/{identifier}"

    if user_id is not None:
        newShortenedUrl = ShortenedUrl(
            url=original_url,
            short_url=shortenedURL,
            user_id=user_id,
        )
        print(newShortenedUrl)
    else:
        newShortenedUrl = ShortenedUrl(
            url=original_url,
            short_url=shortenedURL,
        )
        print(newShortenedUrl)

    saveToDatabase(db, newShortenedUrl)

    return newShortenedUrl
