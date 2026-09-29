from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.api.v1.router import api_router
from app.models import user, course, lab, quiz, tool, event, progress  # noqa: F401

Base.metadata.create_all(bind=engine)

app = FastAPI(title="CyberSec Academy API", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def root():
    return {"status": "ok", "service": "cybersec-academy", "version": "0.2.0"}
