from fastapi import APIRouter

from routers import (
    users, groups, projects, works, studies,
    hobbies, competences, events
)


api_router = APIRouter()


api_router.include_router(users.router, prefix='/user', tags=['User'])
api_router.include_router(groups.router, prefix='/group', tags=['Group'])
api_router.include_router(projects.router, prefix='/project', tags=['Project'])
api_router.include_router(works.router, prefix='/work', tags=['Work'])
api_router.include_router(studies.router, prefix='/study', tags=['Study'])
api_router.include_router(hobbies.router, prefix='/hobby', tags=['Hobby'])
api_router.include_router(competences.router, prefix='/competence', tags=['Competence'])
api_router.include_router(events.router, prefix='/event', tags=['Event'])