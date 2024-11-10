from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware


from app.core.settings import settings
from app.api.v1.endpoints.auth import oauth2_scheme
from app.api.v1.endpoints.auth import router_auth

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)


app.include_router(router_auth)


@app.get("/")  # TODO: TRASH
async def root(auth=Depends(oauth2_scheme)):
    return {"message": "Hello World"}
