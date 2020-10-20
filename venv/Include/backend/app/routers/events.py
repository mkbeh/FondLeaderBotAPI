from typing import List

from fastapi import FastAPI, HTTPException, APIRouter, Depends, BackgroundTasks
from pydantic import BaseModel

from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise

import random
import string
import datetime
from models import Event_Pydantic, EventIn_Pydantic, EventResponse_Pydantic, EventResponseIn_Pydantic, Events, EventResponses


router = APIRouter()

class Status(BaseModel):
    message: str

@router.get('/events', response_model=List[Event_Pydantic])
async def get_all_events():
    return await Event_Pydantic.from_queryset(Events.all())


@router.post("/", response_model=Event_Pydantic)
async def create_event(event: EventIn_Pydantic):
    event_obj = await Events.create(**event.dict(exclude_unset=True))
    return await Event_Pydantic.from_tortoise_orm(event_obj)


@router.post("/eventsresponse", response_model=EventResponse_Pydantic)
async def create_response(response: EventResponseIn_Pydantic):
    response_obj = await EventResponses.create(**response.dict(exclude_unset=True))
    return await EventResponse_Pydantic.from_tortoise_orm(response_obj)


@router.get(
    "/eventresponse/{event}", response_model=List[EventResponse_Pydantic]
)
async def get_event_responses(event: str):
    return await EventResponse_Pydantic.from_queryset(EventResponses.filter(event=event).all())