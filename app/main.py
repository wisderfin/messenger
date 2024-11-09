from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware


from core import settings
from api.v1.endpoints.auth import oauth2_scheme
from api.v1.endpoints.auth import router_auth as auth_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)


app.include_router(auth_router)


@app.get("/")  # TODO: TRASH
async def root(auth=Depends(oauth2_scheme)):
    return {"message": "Hello World"}
