from fastapi import APIRouter, HTTPException, status
from models.users import User, UserLogIn
from database.connection import Database

user_router = APIRouter(tags=["User"])
user_db = Database(User)


@user_router.post("/signup")
async def register_user(user: User) -> dict:
    _user = await User.find_one(User.email == user.email)

    if _user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already existed",
        )
    await user_db.save(user)

    return {"message": "User successfully registered!"}


@user_router.post("/login")
async def user_login(user: UserLogIn) -> dict:
    _user = await User.find_one(User.email == user.email)

    if not _user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if _user.password != user.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong credentials",
        )
    return {"message": "Login successfully!!!"}
