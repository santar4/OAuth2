from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.user import InputUserData, ListBaseUsers, UserBase

from models.user import User
from settings import get_session
from werkzeug.security import generate_password_hash
from routes.auth import get_current_user, get_current_admin

route = APIRouter()


@route.post("/")
async def registration(data_user: InputUserData,
                       session: AsyncSession = Depends(get_session)) -> UserBase:
    stmt = select(User).filter_by(email=data_user.email)
    user = await session.scalar(stmt)
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is exists")

    user_dict = data_user.model_dump()
    user_dict["password_hash"] = generate_password_hash(user_dict["password"])
    del user_dict["password_repeat"]
    del user_dict["password"]

    new_user = User(**user_dict)

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return UserBase.model_validate(new_user)


@route.get("/read_all/")
async def get_all_users(session: AsyncSession = Depends(get_session),
                        _=Depends(get_current_admin)) -> ListBaseUsers:
    users = await session.scalars(select(User))
    count = await session.scalar(select(func.count()).select_from(User))
    return ListBaseUsers(users=users, count_users=count)
