from exceptions.exceptions import IncorrectPasswordException, UserDoesNotExistException
from fastapi.security import OAuth2PasswordBearer
from dto.responseDTO import GetUserResponseDTO
from fastapi import Depends, HTTPException
from passlib.context import CryptContext
from models.schemas import LoginForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from models.models import User
from datetime import datetime
from typing import Annotated, Optional
from starlette import status
import os


SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth_bearer = OAuth2PasswordBearer(tokenUrl="user/login")
optional_oauth_bearer = OAuth2PasswordBearer(tokenUrl="user/login", auto_error=False)


def checkExistingUser(username: str, db: Session) -> bool:
    """
    Check if user exists in the database.
    """

    user = db.query(User).filter(User.username == username).first()
    return True if user else False


def hashPassword(password: str) -> str:
    """
    Hash a password for the first time, with a randomly-generated salt.
    """

    return bcrypt_context.hash(password)


def authenticateUser(formData: LoginForm, db: Session) -> User:
    """
    Check if user exists and if password is correct.
    """

    user = db.query(User).filter(User.username == formData.username).first()
    if not user:
        raise UserDoesNotExistException()
    else:
        if not bcrypt_context.verify(formData.password, user.password):
            raise IncorrectPasswordException()
        else:
            return user


def createAccessToken(user: User, expires_in: int) -> str:
    """
    Creates an access token for the requested user, which will expire in the given amount of time.
    """

    expires = datetime.utcnow() + expires_in
    encoded_data = {
        "sub": user.username,
        "id": str(user.id),
        "exp": expires,
    }

    encoded_jwt = jwt.encode(encoded_data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def getCurrentUser(token: Annotated[str, Depends(oauth_bearer)]) -> GetUserResponseDTO:
    """
    Middleware function of the application to check whether the user is authenticated or not.

    Returns the user's id and username if access token is valid, else raises an exception.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        exp: int = payload.get("exp")

        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user.",
            )

        if datetime.utcnow() > datetime.utcfromtimestamp(exp):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access token has expired. Please login again.",
            )
        return GetUserResponseDTO(is_valid=True, id=user_id, username=username)

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user.",
        )

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"{e}")


def getOptionalCurrentUser(
    token: str | None = Depends(optional_oauth_bearer),
) -> GetUserResponseDTO | None:
    """
    Optional middleware function of the application to check whether the user is authenticated or not.

    Returns the user's id and username if access token is valid, else returns None.
    """
    try:
        if token:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            user_id: int = payload.get("id")
            exp: int = payload.get("exp")

            if datetime.utcnow() > datetime.utcfromtimestamp(exp):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Access token has expired. Please login again.",
                )
            return GetUserResponseDTO(is_valid=True, id=user_id, username=username)
        else:
            return None

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user.",
        )

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"{e}")
