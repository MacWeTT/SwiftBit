from pydantic import BaseModel, validator


class LoginRequestDTO(BaseModel):
    username: str
    password: str

    @validator("password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be atleast 8 characters long.")
        return v


class CreateUserRequestDTO(BaseModel):
    username: str
    password: str


class DelelteUserRequestDTO(BaseModel):
    username: str
