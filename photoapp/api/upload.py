from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

# from api.dependencies import session_dependency
from api.dependencies import templates
from api.dependencies import user_dependency


router = APIRouter(
    prefix='/upload',
    tags=['Upload']
)


@router.get("", response_class=HTMLResponse)
async def home_page(request: Request, user: user_dependency):
    return templates.TemplateResponse(
        'upload.html',
        {
            'request': request,
            'user': user
        }
    )