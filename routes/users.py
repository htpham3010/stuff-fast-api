from fastapi import APIRouter, HTTPException, status
from models.users import User, UserLogIn

user_router = APIRouter(tags=["User"])
users = {}


@user_router.post("/signup")
async def register_user(data: User) -> dict:
    if data.email in users:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already existed",
        )
    users[data.email] = data
    return {"message": "User successfully registered!"}


@user_router.post("/login")
async def user_login(user: UserLogIn) -> dict:
    if users[user.email] not in users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    if users[user.email].password != user.password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Wrong credentials"
        )
    return {"message": "Login successfully!!!"}
