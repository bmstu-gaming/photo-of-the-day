from authlib.integrations.starlette_client import OAuth, OAuthError
from fastapi import APIRouter, Request
from starlette.config import Config
from starlette.responses import RedirectResponse

from config.settings import settings

from api.dependencies import templates

router = APIRouter(
    prefix="/discord",
    tags=["Discord SSO"]
)

config = Config(environ={
    'DISCORD_CLIENT_ID': settings.auth.discord_client_id,
    'DISCORD_CLIENT_SECRET': settings.auth.discord_client_secret,
    'SECRET_KEY': settings.auth.secret_key
})

oauth = OAuth(config)

oauth.register(
    name='discord',
    api_base_url='https://discord.com/api',
    access_token_url='https://discord.com/api/oauth2/token',
    authorize_url='https://discord.com/oauth2/authorize',
    userinfo_endpoint='https://discord.com/api/users/@me',
    client_kwargs={
        'scope': 'identify email',
        'timeout': 30,
    },
)


# Used as callback for discord
@router.get("/auth", name="discord_auth")
async def authorize(request: Request):
    try:
        token = await oauth.discord.authorize_access_token(request)

    except OAuthError as e:
        return templates.TemplateResponse(
            'error.html',
            {
                'error_message': e.error
            }
        )
    # user = token.get('userinfo')
    # user = await get_user_data(oauth=oauth, token=token)
    user = await get_user_data(oauth=oauth, token=token)
    print(user)
    if user:
       request.session['user'] = dict(user)
    return RedirectResponse(url='/home')


@router.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for("discord_auth")
    return await oauth.discord.authorize_redirect(request, redirect_uri)


@router.get("/logout")
async def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url='/home')


async def get_user_data(oauth, token):
    """
    This is the way to get user info
    """
    response = await oauth.discord.userinfo(token=token)
    # if response.status != 200:
    #     return None
    print(response)
    return response