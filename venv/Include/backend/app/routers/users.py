from typing import List

from fastapi import FastAPI, HTTPException, APIRouter, Depends, BackgroundTasks
from pydantic import BaseModel

from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise

import random
import string
import datetime
from models import *


router = APIRouter()

class Status(BaseModel):
    message: str

@router.get("/", response_model=List[User_Pydantic])
async def get_users():
    return await User_Pydantic.from_queryset(Users.all())


@router.get(
    "/group/{group_id}", response_model=List[User_Pydantic]
)
async def get_group_users(group_id: int):
    return await User_Pydantic.from_queryset(Users.filter(group=group_id).all())


@router.post("/check_password")
async def check_password_and_start_registration(password: str, telid: int):
    corr_pwd = ['MENTOR', 'MEMBER']
    ans = False
    try:
        if corr_pwd.index(password) > -1:
            def buildblock(size):
                return ''.join(random.choice(string.ascii_letters) for _ in range(size))
            token = buildblock(12)
            user = {
                "telegram_id": telid,
                "first_name": "awaiting",
                "last_name": "awaiting",
                "role": "awaiting",
                "city": "awaiting",
                "startdate": datetime.date.today(),
                "email": "awaiting",
                "fb": "awaiting",
                "vk": "awaiting",
                "telnum": "awaiting",
                "birthday": datetime.date.today(),
                "group": "awaiting",
                "token": token,
                "roots": 0
            }
            user_obj = await Users.create(**user)
            user = await User_Pydantic.from_tortoise_orm(user_obj)
            answ = token
        return {'token': answ, 'id': user.id}
    except:
        return {'token': ans, 'id': ans}


@router.post(
    "/{user_id}/{token}", response_model=User_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def update_user(user_id: int, token: str, user: UserIn_Pydantic):
    await Users.filter(id=user_id, token=token).update(**user.dict(exclude_unset=True))
    return await User_Pydantic.from_queryset_single(Users.get(id=user_id))


@router.delete("/{token}/{user_id}", response_model=Status, responses={404: {"model": HTTPNotFoundError}})
async def delete_user(user_id: int, token: str):
    deleted_count = await Users.filter(id=user_id, token=token).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return Status(message=f"Deleted user {user_id}")


@router.get(
    "/{user_id}", response_model=User_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def get_user(user_id: int):
    return await User_Pydantic.from_queryset_single(Users.get(id=user_id))


@router.get(
    "/search/ln/{last_name}", response_model=List[User_Pydantic]
)
async def get_by_last_name(last_name: str):
    return await User_Pydantic.from_queryset(Users.filter(last_name=last_name).all())


@router.get(
    "/search/tg/{telegram_id}", response_model=List[User_Pydantic]
)
async def get_by_telegramid(telegram_id: str):
    return await User_Pydantic.from_queryset(Users.filter(telegramid=telegram_id).all())


@router.get(
    "/search/vk/{vk}", response_model=List[User_Pydantic]
)
async def get_by_vk(vk: str):
    return await User_Pydantic.from_queryset(Users.filter(vk=vk).all())


@router.get(
    "/search/fb/{fb}", response_model=List[User_Pydantic]
)
async def get_by_fb(fb: str):
    return await User_Pydantic.from_queryset(Users.filter(fb=fb).all())


@router.get("/events/{telegram_id}/{token}", response_model=List[Event_Pydantic])
async def get_user_events(telegram_id: int, token: str):
    user = await User_Pydantic.from_queryset(Users.filter(telegram_id=telegram_id, token=token).all())
    if user != []:
        local_group = user[0].group
        global_group = local_group.split('-')[0] + '-' + local_group.split('-')[1]
        total_group = local_group.split('-')[0]
        return await Event_Pydantic.from_queryset(Events.filter(trajectory__in=[local_group, global_group, total_group]).all())



