from authlib.integrations.starlette_client import OAuth, OAuthError
from fastapi import APIRouter, Request
from starlette.config import Config
from starlette.responses import RedirectResponse

from config.settings import settings

from api.dependencies import templates

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
async def authorize(request: Request):
    try:
        token = await oauth.github.authorize_access_token(request)

    except OAuthError as e:
        return templates.TemplateResponse(
            'error.html',
            {
                'error_message': e.error
            }
        )
    user = await oauth.github.userinfo(token=token)
    print(user)
    if user:
        request.session['user'] = {
            'id': dict(user)['id'],
            'username': dict(user)['login'],
        }
    
    # To save to database:

    # sso_id = user['id']
    # username = user['login']
    # avatar_url = user['https://avatars.githubusercontent.com/u/37626963?v=4']

    return RedirectResponse(url='/home')


@router.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for("github_auth")
    return await oauth.github.authorize_redirect(request, redirect_uri)
