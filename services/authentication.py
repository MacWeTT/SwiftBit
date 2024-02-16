from datetime import datetime
from sqlalchemy.orm import Session
from exceptions.exceptions import IncorrectPasswordException, UserDoesNotExistException
from models.models import User
from passlib.context import CryptContext
from jose import JWTError, jwt

from models.schemas import LoginForm


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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


SECRET_KEY = "c7be378f33d682002ba1784011a6edfa535e18a50994227de1647d8d5fd728e7"
ALGORITHM = "HS256"


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
