from typing import List

from fastapi import FastAPI, HTTPException, APIRouter, Depends, BackgroundTasks
from pydantic import BaseModel

from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise

import random
import string
import datetime

from models import User_Pydantic, UserIn_Pydantic, Hobby_Pydantic, HobbyIn_Pydantic, Users, Hobbies


router = APIRouter()

class Status(BaseModel):
    message: str
    
@router.get(
    "/{telegram_id}", response_model=List[Hobby_Pydantic]
)
async def get_user_hobbies(telegram_id: int):
    return await Hobby_Pydantic.from_queryset(Hobbies.filter(telegram_id=telegram_id).all())


@router.get("/{telegram_id}/{token}/{hashtag}", response_model=Hobby_Pydantic)
async def create_hobby(telegram_id: int, token: str, hashtag: str):
    user = await User_Pydantic.from_queryset(Users.filter(telegram_id=telegram_id, token=token).all())
    if user != []:
        hobby = {
            "hashtag": hashtag,
            "userid": telegram_id
        }
        hobby_obj = await Hobbies.create(**hobby)
        return await Hobby_Pydantic.from_tortoise_orm(hobby_obj)


@router.delete("/{telegram_id}/{token}/{hobby_id}", response_model=Status, responses={404: {"model": HTTPNotFoundError}})
async def delete_hobby(hobby_id: int, telegram_id: int, token: str):
    user = await User_Pydantic.from_queryset(Users.filter(telegram_id=telegram_id, token=token).all())
    if user != []:
        deleted_count = await Hobbies.filter(id=hobby_id).delete()
        if not deleted_count:
            raise HTTPException(status_code=404, detail=f"Hobby {hobby_id} not found")
        return Status(message=f"Deleted hobby {hobby_id}")
