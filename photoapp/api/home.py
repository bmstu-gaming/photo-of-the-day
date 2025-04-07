from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse

# from api.dependencies import session_dependency
from api.dependencies import templates
from api.dependencies import user_dependency


router = APIRouter(
    prefix='/home',
    tags=['Home']
)


# TODO: add user responce model
@router.get("", response_class=HTMLResponse)
async def home_page(request: Request, user: user_dependency):
    user = request.session.get('user')
    return templates.TemplateResponse(
        'home.html',
        {
            'request': request,
            'user': user
        }
    )

    