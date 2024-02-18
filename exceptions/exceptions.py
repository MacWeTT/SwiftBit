from fastapi import HTTPException


class BaseException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)
        self.code = status_code


class UserDoesNotExistException(BaseException):
    def __init__(self):
        super().__init__(status_code=404, detail="User does not exist")


class UserAlreadyExistsException(BaseException):
    """
    User already exists in the database.
    """

    def __init__(self):
        super().__init__(
            status_code=400, detail="User already exists. Please try to login instead."
        )


class IncorrectPasswordException(BaseException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Incorrect password. Make sure your password is correct.",
        )
