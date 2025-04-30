from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

# from api.dependencies import session_dependency
from api.dependencies import templates
from api.dependencies import user_dependency


router = APIRouter(
    prefix='/upload',
    tags=['Upload']
)

# TODO: add FileUpload
# @router.get("", response_class=HTMLResponse)
# async def upload(request: Request, user: user_dependency):
#     pass
