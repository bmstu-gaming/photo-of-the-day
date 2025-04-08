from authlib.integrations.starlette_client import OAuth, OAuthError
from fastapi import APIRouter, Request
from starlette.config import Config
from starlette.responses import RedirectResponse

from config.settings import settings

from api.dependencies import templates, session_dependency
from api.auth import save_user_session
import crud.users as crud_users

from schemas.user import UserCreate

PROVIDER='github'

router = APIRouter(
    prefix="/github",
    tags=["Github SSO"]
)

config = Config(environ={
    'GITHUB_CLIENT_ID': settings.auth.github_client_id,
    'GITHUB_CLIENT_SECRET': settings.auth.github_client_secret,
    'SECRET_KEY': settings.auth.secret_key
})

oauth = OAuth(config)

oauth.register(
    name='github',
    api_base_url='https://api.github.com/',
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
    userinfo_endpoint='https://api.github.com/user',
    client_kwargs={
        'scope': 'read:user',
        'timeout': 30,
    },
)


# Used as callback for github
@router.get("/auth", name="github_auth")
async def authorize(
    request: Request,
    session: session_dependency
):
    # Getting token (required only to get user info, we do not save it)
    try:
        token = await oauth.github.authorize_access_token(request)
    except OAuthError as e:
        return templates.TemplateResponse(
            'error.html', {'error_message': e.error}
        )
    # Getting user info
    user = await oauth.github.userinfo(token=token)
    if not user:
        return templates.TemplateResponse(
            'error.html', {'error_message': "Could not get user info!"}
        )
    user_dict = dict(user)
    
    save_user_session(request=request, user_id=user_dict['id'], provider=PROVIDER)
    
    user_schema = UserCreate(
        sso_id=user_dict['id'],
        sso_provider=PROVIDER,
        username=user_dict['login'],
        avatar_url=user_dict['avatar_url']
    )

    await crud_users.create_user_if_not_exist(session=session, user_schema=user_schema)

    return RedirectResponse(url='/home')


@router.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for("github_auth")
    return await oauth.github.authorize_redirect(request, redirect_uri)
