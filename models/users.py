from pydantic import BaseModel, EmailStr
from beanie import Document


class User(Document):
    email: EmailStr
    password: str

    class Settings:
        name = "users"

    class Config:
        schema_extra = {
            "example": {
                "email": "fastapi@example.com",
                "password": "stuffastapi",
            }
        }


class UserLogIn(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
