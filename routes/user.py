from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from dto.responseDTO import CreateUserResponseDTO, LoginResponseDTO
from fastapi import Depends, HTTPException, APIRouter
from datetime import timedelta
from typing import Annotated
from starlette import status
from models.models import User

# Fetch and use DB
from database.databaseUtil import db_dependency

# DTO
from dto.requestDTO import CreateUserRequestDTO

# Services
from services.authentication import (
    authenticateUser,
    checkExistingUser,
    createAccessToken,
    hashPassword,
)

# Exceptions
from exceptions.exceptions import UserAlreadyExistsException

userRouter = APIRouter(prefix="/user")

oauth_bearer = OAuth2PasswordBearer(tokenUrl="user/login")


@userRouter.post("/register")
async def create_user(db: db_dependency, user_request: CreateUserRequestDTO):
    try:
        if checkExistingUser(user_request.username, db):
            raise UserAlreadyExistsException()
        else:
            user = User(
                username=user_request.username,
                password=hashPassword(user_request.password),
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            return CreateUserResponseDTO(
                message="User created successfully. Please login to continue.",
                username=user.username,
            )
    except Exception as e:
        print(e)
        raise e


@userRouter.post("/login", response_model=LoginResponseDTO)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency,
):
    try:
        user = authenticateUser(form_data, db)
        token = createAccessToken(user, timedelta(minutes=30))
        return LoginResponseDTO(
            access_token=token,
            token_type="bearer",
        )
    except Exception as e:
        print(e)
        raise e
