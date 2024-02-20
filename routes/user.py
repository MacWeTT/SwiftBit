from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, APIRouter, HTTPException
from models.models import User
from datetime import timedelta
from typing import Annotated
from starlette import status

# Fetch and use DB
from database.databaseUtil import db_dependency, user_dependency
from database.dbFuncs import deleteFromDatabase, saveToDatabase

# DTO
from dto.responseDTO import CreateUserResponseDTO, LoginResponseDTO, ResponseDTO
from dto.requestDTO import CreateUserRequestDTO, EditUserRequestDTO

# Exceptions
from exceptions.exceptions import UserAlreadyExistsException

# Services
from services.authentication import (
    createAccessToken,
    checkExistingUser,
    authenticateUser,
    hashPassword,
)


userRouter = APIRouter(prefix="/user")


@userRouter.post("/register")
async def create_user(db: db_dependency, user_request: CreateUserRequestDTO):
    """
    Create a new user in the database.
    """
    try:
        if checkExistingUser(user_request.username, db):
            raise UserAlreadyExistsException()
        else:
            user = User(
                username=user_request.username,
                password=hashPassword(user_request.password),
            )
            saveToDatabase(db, user)
            message = "User created successfully. Please login to continue."
            return CreateUserResponseDTO(message=message, username=user.username)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")


@userRouter.post("/login", response_model=LoginResponseDTO)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency,
):
    """
    Login a user so that URLs can be managed.

    Returns a JSON Web Token as a response.
    """
    try:
        user = authenticateUser(form_data, db)
        token = createAccessToken(user, timedelta(minutes=30))
        return LoginResponseDTO(token_type="Bearer", access_token=token)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")


@userRouter.patch("/edit-user")
async def edit_user(
    user: user_dependency, db: db_dependency, request: EditUserRequestDTO
):
    """
    Edit the details of the logged in user.

    Currently the service only supports editing the user's username.
    """
    try:
        query = db.query(User).filter(User.username == user.username).first()
        query.username = request.username
        saveToDatabase(db, query)
        message = f"User {user.username} has been successfully edited to {request.username}. Please login again to avoid any errors."
        return ResponseDTO(message=message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")


@userRouter.delete("/delete-user")
async def delete_user(user: user_dependency, db: db_dependency):
    """
    Delete a user from the database.

    The user must be logged in, else it cannot be deleted.

    If you face a bad request, there is a chance that your user has been already deleted.
    """
    try:
        query = db.query(User).filter(User.username == user.username).first()
        deleteFromDatabase(db, query)
        message = f"User {user.username} has been deleted successfully."
        return ResponseDTO(message=message)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")
