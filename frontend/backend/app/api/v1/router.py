from fastapi import APIRouter
from app.api.v1 import users, courses, labs, quizzes

api_router = APIRouter()
api_router.include_router(users.router)
api_router.include_router(courses.router)
api_router.include_router(labs.router)
api_router.include_router(quizzes.router)
