from typing import Optional
from datetime import datetime
from fastapi import HTTPException
from jose import jwt, JWTError

# JWT Configuration
SECRET_KEY = "9ryn23895v2gj4912g34n1x014v24c2m04x"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRY = 30


def create_token(data: dict, expires=Optional[int]):
    to_encode = data.copy()
    if expires:
        to_encode.update({"exp": datetime.now() + expires})
    else:
        to_encode.update({"exp": datetime.now() + ACCESS_TOKEN_EXPIRY})

    jwtToken = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return jwtToken


def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return HTTPException(
            status_code=401,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
