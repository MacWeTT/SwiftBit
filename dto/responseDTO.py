from pydantic import BaseModel


class LoginResponseDTO(BaseModel):
    access_token: str
    token_type: str


class CreateUserResponseDTO(BaseModel):
    message: str
    username: str


class ResponseDTO(BaseModel):
    message: str


class ShortenUrlResponseDTO(BaseModel):
    message: str
    original_url: str
    shortened_url: str
