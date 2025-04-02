from contextlib import asynccontextmanager

import uvicorn

from fastapi import FastAPI
# Increase JSON working speed
from fastapi.responses import ORJSONResponse 

from config.settings import settings
from models import database_manager, ModelBase

from api import router


# New way to do thing on startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    # Uncomment this to autocreate tables on startup, however Alembic ir preferred
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
photo_app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(
        "main:photo_app", 
        host=settings.app.host, 
        port=settings.app.port, 
        reload=True
    )