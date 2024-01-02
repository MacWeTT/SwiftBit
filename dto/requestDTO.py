from pydantic import BaseModel, validator


class LoginRequestDTO(BaseModel):
    username: str
    password: str

    # @validator("email")
    # def validate_email(cls, v):
    #     pass

    # @validator("password")
    # def validate_password(cls, v):
    #     pass


class CreateUserRequestDTO(BaseModel):
    username: str
    password: str
