from typing import List

from fastapi import FastAPI, HTTPException, APIRouter, Depends, BackgroundTasks
from pydantic import BaseModel

from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise

import random
import string
import datetime

from models import User_Pydantic, UserIn_Pydantic, Study_Pydantic, StudyIn_Pydantic, Users, Studies


router = APIRouter()

class Status(BaseModel):
    message: str

@router.get(
    "/user/{telegram_id}", response_model=List[Study_Pydantic]
)
async def get_user_studies(telegram_id: int):
    return await Study_Pydantic.from_queryset(Studies.filter(telegram_id=telegram_id).all())


@router.post("/{telegram_id}/{token}", response_model=Study_Pydantic)
async def create_study(telegram_id: int, token: str, study: StudyIn_Pydantic):
    user = await User_Pydantic.from_queryset(Users.filter(telegram_id=telegram_id, token=token).all())
    if user != []:
        study_obj = await Studies.create(**study.dict(exclude_unset=True))
        return await Study_Pydantic.from_tortoise_orm(study_obj)


@router.delete("/{telegram_id}/{token}/{study_id}", response_model=Status, responses={404: {"model": HTTPNotFoundError}})
async def delete_study(study_id: int, telegram_id: int, token: str):
    user = await User_Pydantic.from_queryset(Users.filter(telegram_id=telegram_id, token=token).all())
    if user != []:
        deleted_count = await Studies.filter(id=study_id).delete()
        if not deleted_count:
            raise HTTPException(status_code=404, detail=f"Study {study_id} not found")
        return Status(message=f"Deleted study {study_id}")