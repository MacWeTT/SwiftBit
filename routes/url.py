from database.databaseUtil import user_dependency, db_dependency
from models.models import ShortenedUrl
from fastapi import APIRouter

urlRouter = APIRouter(prefix="/url")


@urlRouter.get("/")
async def get_user_urls(user: user_dependency, db: db_dependency):
    try:
        urls = db.query(ShortenedUrl).filter(ShortenedUrl.user_id == user["id"]).first()
        return {"urls": urls}
    except Exception as e:
        print(e)
        raise e
