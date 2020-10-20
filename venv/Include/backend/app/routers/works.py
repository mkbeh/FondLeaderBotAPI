from typing import List

from fastapi import FastAPI, HTTPException, APIRouter, Depends, BackgroundTasks
from pydantic import BaseModel

from tortoise.contrib.fastapi import HTTPNotFoundError

import random
import string
import datetime

from models import User_Pydantic, UserIn_Pydantic, Work_Pydantic, WorkIn_Pydantic, Users, Works




router = APIRouter()

class Status(BaseModel):
    message: str

@router.get(
    "/user/{telegram_id}", response_model=List[Work_Pydantic]
)
async def get_user_works(telegram_id: int):
    return await Work_Pydantic.from_queryset(Works.filter(telegram_id=telegram_id).all())


@router.post("/{telegram_id}/{token}", response_model=Work_Pydantic)
async def create_work(telegram_id: int, token: str, work: WorkIn_Pydantic):
    user = await User_Pydantic.from_queryset(Users.filter(telegram_id=telegram_id, token=token).all())
    if user != []:
        work_obj = await Works.create(**work.dict(exclude_unset=True))
        return await Work_Pydantic.from_tortoise_orm(work_obj)


@router.delete("/{telegram_id}/{token}/{work_id}", response_model=Status, responses={404: {"model": HTTPNotFoundError}})
async def delete_work(work_id: int, telegram_id: int, token: str):
    user = await User_Pydantic.from_queryset(Users.filter(telegram_id=telegram_id, token=token).all())
    if user != []:
        deleted_count = await Works.filter(id=work_id).delete()
        if not deleted_count:
            raise HTTPException(status_code=404, detail=f"Work {work_id} not found")
        return Status(message=f"Deleted work {work_id}")