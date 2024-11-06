from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware


from app.dependes import get_async_session
from app.routers.auth import oauth2_scheme
from app.utils.auth import UsersUtils

from .settings import settings
from app.routers import auth_router

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)

app.include_router(auth_router)

@app.get("/")
async def root(auth = Depends(oauth2_scheme)):
    return {"message": "Hello World"}
