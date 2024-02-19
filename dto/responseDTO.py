from pydantic import BaseModel


class ResponseDTO(BaseModel):
    message: str


class LoginResponseDTO(BaseModel):
    access_token: str
    token_type: str


class CreateUserResponseDTO(BaseModel):
    message: str
    username: str


class GetUserResponseDTO(BaseModel):
    id: int
    username: str


class GetAllShortenedUrlsDTO(BaseModel):
    short_url: str
    url: str


class ShortenUrlResponseDTO(BaseModel):
    message: str
    original_url: str
    shortened_url: str
