from fastapi import APIRouter, HTTPException, Depends, status
from auth.hash_password import HashPassword
from models.users import User, TokenResponse
from database.connection import Database
from fastapi.security import OAuth2PasswordRequestForm
from auth.jwt_handler import create_access_token


user_router = APIRouter(tags=["User"])
user_db = Database(User)
_hash_pwd = HashPassword()


@user_router.post("/signup")
async def register_user(user: User) -> dict:
    _user = await User.find_one(User.email == user.email)

    if _user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already existed",
        )
    user.password = _hash_pwd.create_hash(user.password)
    await user_db.save(user)

    return {"message": "User successfully registered!"}


@user_router.post("/login", response_model=TokenResponse)
async def user_login(user: OAuth2PasswordRequestForm = Depends()) -> dict:
    _user = await User.find_one(User.email == user.username)

    if not _user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if not _hash_pwd.verify_hash(user.password, _user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong credentials",
        )

    return {
        "access_token": create_access_token(_user.email),
        "token_type": "Bearer",
    }
