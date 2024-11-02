from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .settings import settings

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)
