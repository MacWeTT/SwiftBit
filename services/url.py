from database.databaseUtil import db_dependency
from database.dbFuncs import saveToDatabase
from models.models import ShortenedUrl
import uuid, os

from services.authentication import getCurrentUser


def createNewShortenedUrl(original_url: str, db: db_dependency, current_user) -> str:
    shortened_identifier = str(uuid.uuid4())[:8]
    base_shortened_url = os.environ.get("API_URL")

    print("Base Url", base_shortened_url)
    shortened_url: str = base_shortened_url + shortened_identifier

    new_shortened_url = ShortenedUrl(
        url=original_url, short_url=shortened_url, user_id=current_user.id
    )
    saveToDatabase(db, new_shortened_url)

    return shortened_url
