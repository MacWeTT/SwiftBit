from email import message
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from dto.responseDTO import CreateUserResponseDTO, LoginResponseDTO, ResponseDTO
from fastapi import Depends, HTTPException, APIRouter
from datetime import timedelta
from typing import Annotated
from starlette import status
from database.dbFuncs import deleteFromDatabase, saveToDatabase
from models.models import User

# Fetch and use DB
from database.databaseUtil import db_dependency

# DTO
from dto.requestDTO import CreateUserRequestDTO, DelelteUserRequestDTO

# Services
from services.authentication import (
    authenticateUser,
    checkExistingUser,
    createAccessToken,
    hashPassword,
)

# Exceptions
from exceptions.exceptions import UserAlreadyExistsException, UserDoesNotExistException

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
            saveToDatabase(db, user)
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
            token_type="Bearer",
            access_token=token,
        )
    except Exception as e:
        print(e)
        raise e


@userRouter.delete("/delete-user")
async def delete_user(db: db_dependency, request: DelelteUserRequestDTO):
    try:
        user = checkExistingUser(request.username, db)
        if user:
            query = db.query(User).filter(User.username == request.username).first()
            deleteFromDatabase(db, query)
            return ResponseDTO(
                message=f"User {request.username} has been deleted successfully."
            )
        else:
            raise UserDoesNotExistException()
    except Exception as e:
        print(e)
        raise e
