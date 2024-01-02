from pydantic import BaseModel


class LoginResponseDTO(BaseModel):
    access_token: str
    token_type: str


class CreateUserResponseDTO(BaseModel):
    message: str
    username: str
