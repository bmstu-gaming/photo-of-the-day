from contextlib import asynccontextmanager
import uvicorn

from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
# ORJSONResponse - Increase JSON working speed
from fastapi.responses import ORJSONResponse
from fastapi.middleware.trustedhost import TrustedHostMiddleware


from config.settings import settings
from database import database_manager
from api import router

# New way to do thing on startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup

    # Uncomment this to autocreate tables on startup, however Alembic is preferred
    # async with database_manager.engine.begin() as conn:
    #     # await conn.run_sync(ModelBase.metadata.create_all)
    #     # await conn.run_sync(ModelBase.metadata.drop_all)

    yield
    # shutdown
    await database_manager.dispose()


photo_app = FastAPI(
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

photo_app.add_middleware(SessionMiddleware, secret_key=settings.auth.secret_key)
photo_app.add_middleware(
    CORSMiddleware, 
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=["*"]
)


# We can setup trusted hosts via settings
if settings.app.allowed_hosts is not None:
    photo_app.add_middleware(
        TrustedHostMiddleware, allowed_hosts=settings.app.allowed_hosts.split(',')
    )


photo_app.include_router(router)
photo_app.mount("/static", StaticFiles(directory="static"), name="static")


if __name__ == "__main__":
    uvicorn.run(
        "main:photo_app", 
        host=settings.app.host, 
        port=settings.app.port, 
        reload=True
    )