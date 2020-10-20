from typing import List

from fastapi import FastAPI, HTTPException, APIRouter, Depends, BackgroundTasks
from pydantic import BaseModel

from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise

import random
import string
import datetime

from models import Group_Pydantic, GroupIn_Pydantic, Groups


router = APIRouter()


@router.get('/', response_model=List[Group_Pydantic])
async def get_groups():
    return await Group_Pydantic.from_queryset(Groups.all())


@router.post("/", response_model=Group_Pydantic)
async def create_group(group: GroupIn_Pydantic):
    group_obj = await Groups.create(**group.dict(exclude_unset=True))
    return await Group_Pydantic.from_tortoise_orm(group_obj)