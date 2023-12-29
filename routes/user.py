from fastapi import APIRouter, Depends

# Fetch and use DB
from database.dbUtil import get_db
from sqlalchemy.orm import Session

userRouter = APIRouter(prefix="/user")


@userRouter.get("/")
async def get_user():
    return {"message": "Get User"}


@userRouter.post("/login")
async def login(db: Session = Depends(get_db), ):
    return {"message": "Login"}
