from contextlib import asynccontextmanager
import uvicorn

from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi import FastAPI, Request, HTTPException
# ORJSONResponse - Increase JSON working speed
from fastapi.responses import ORJSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.trustedhost import TrustedHostMiddleware


from config.settings import settings
from database import database_manager
from api import router
from api.dependencies import session_dependency

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

# NOTE: may be better way?
photo_app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=["bmstu.org", "*.bmstu.org", "localhost"]
)


photo_app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(
        "main:photo_app", 
        host=settings.app.host, 
        port=settings.app.port, 
        reload=True
    )