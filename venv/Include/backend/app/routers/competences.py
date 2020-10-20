from typing import List

from fastapi import FastAPI, HTTPException, APIRouter, Depends, BackgroundTasks
from pydantic import BaseModel

from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise

import random
import string
import datetime

from models import User_Pydantic, Competence_Pydantic, CompetenceIn_Pydantic, Users, Competences


router = APIRouter()

class Status(BaseModel):
    message: str

@router.get(
    "/{telegram_id}", response_model=List[Competence_Pydantic]
)
async def get_user_competences(telegram_id: int):
    return await Competence_Pydantic.from_queryset(Competences.filter(telegram_id=telegram_id).all())


@router.get(
    "/competences/users/{hashtag}", response_model=List[User_Pydantic]
)
async def get_users_by_competence(hashtag: str):
    competences = await Competence_Pydantic.from_queryset(Competences.filter(hashtag=hashtag).all())
    listusers = []
    response = []
    for competence in competences:
        listusers.append(competence.userid)
    for id in listusers:
        user = await User_Pydantic.from_queryset_single(Users.get(telegram_id=id))
        response.append(user)
    return response


@router.get("/{telegram_id}/{token}/{hashtag}", response_model=Competence_Pydantic)
async def create_competence(telegram_id: int, token: str, hashtag: str):
    user = await User_Pydantic.from_queryset(Users.filter(telegram_id=telegram_id, token=token).all())
    if user != []:
        competence = {
            "hashtag": hashtag,
            "userid": telegram_id
        }
        competence_obj = await Competences.create(**competence)
        return await Competence_Pydantic.from_tortoise_orm(competence_obj)


@router.delete("/{telegram_id}/{token}/{competence_id}", response_model=Status, responses={404: {"model": HTTPNotFoundError}})
async def delete_competence(competence_id: int, telegram_id: int, token: str):
    user = await User_Pydantic.from_queryset(Users.filter(telegram_id=telegram_id, token=token).all())
    if user != []:
        deleted_count = await Competences.filter(id=competence_id).delete()
        if not deleted_count:
            raise HTTPException(status_code=404, detail=f"Competence {competence_id} not found")
        return Status(message=f"Deleted competence {competence_id}")