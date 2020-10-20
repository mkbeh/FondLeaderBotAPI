from typing import List

from fastapi import FastAPI, HTTPException, APIRouter, Depends, BackgroundTasks
from pydantic import BaseModel

from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise

import random
import string
import datetime

from models import User_Pydantic, UserIn_Pydantic, Project_Pydantic, ProjectIn_Pydantic, Users, Projects


router = APIRouter()

class Status(BaseModel):
    message: str

@router.get(
    "/user/{telegram_id}", response_model=List[Project_Pydantic]
)
async def get_user_projects(telegram_id: int):
    return await Project_Pydantic.from_queryset(Projects.filter(telegram_id=telegram_id).all())


@router.post("/{telegram_id}/{token}", response_model=Project_Pydantic)
async def create_project(telegram_id: int, token: str, project: ProjectIn_Pydantic):
    user = await User_Pydantic.from_queryset(Users.filter(telegram_id=telegram_id, token=token).all())
    if user != []:
        project_obj = await Projects.create(**project.dict(exclude_unset=True))
        return await Project_Pydantic.from_tortoise_orm(project_obj)


@router.delete("/{telegram_id}/{token}/{project_id}", response_model=Status, responses={404: {"model": HTTPNotFoundError}})
async def delete_project(project_id: int, telegram_id: int, token: str):
    user = await User_Pydantic.from_queryset(Users.filter(telegram_id=telegram_id, token=token).all())
    if user != []:
        deleted_count = await Projects.filter(id=project_id).delete()
        if not deleted_count:
            raise HTTPException(status_code=404, detail=f"Project {project_id} not found")
        return Status(message=f"Deleted project {project_id}")