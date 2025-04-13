from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse

# from api.dependencies import session_dependency
from api.dependencies import templates
from api.dependencies import user_dependency


router = APIRouter(
    prefix='/gallery',
    tags=['Gallery']
)


@router.get("", response_class=HTMLResponse)
async def gallery(request: Request, user: user_dependency):
    return templates.TemplateResponse(
        'gallery.html',
        {
            'request': request,
            'user': user
        }
    )