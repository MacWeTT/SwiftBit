from datetime import datetime
from sqlalchemy.orm import Session
from exceptions.exceptions import IncorrectPasswordException, UserDoesNotExistException
from models.models import User
from passlib.context import CryptContext
from jose import JWTError, jwt

from models.schemas import LoginForm


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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


SECRET_KEY = "oirhm34r890c4wehmvvn87532g48c237rg0m4c712x12mwevm0rhx102xmvnh0x1384310x1weorth8eovt"
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
