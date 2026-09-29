from fastapi import APIRouter
from app.api.v1 import auth, users, courses, labs, quizzes, tools, events, dashboard, leaderboard

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(courses.router)
api_router.include_router(labs.router)
api_router.include_router(quizzes.router)
api_router.include_router(tools.router)
api_router.include_router(events.router)
api_router.include_router(dashboard.router)
api_router.include_router(leaderboard.router)
