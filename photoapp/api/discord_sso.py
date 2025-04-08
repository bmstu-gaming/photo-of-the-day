from authlib.integrations.starlette_client import OAuth, OAuthError
from fastapi import APIRouter, Request
from starlette.config import Config
from starlette.responses import RedirectResponse

from config.settings import settings

from api.dependencies import templates, session_dependency
from api.auth import save_user_session

from schemas.user import UserCreate
import crud.users as crud_users


PROVIDER = 'discord'

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
        'scope': 'identify',
        'timeout': 30,
    },
)


# Used as callback for discord
# This is the URL that discord will redirect to after the user has authorized the app
@router.get("/auth", name="discord_auth")
async def authorize(
    request: Request,
    session: session_dependency
):
    # Getting token (required only to get user info, we do not save it)
    try:
        token = await oauth.discord.authorize_access_token(request)
    except OAuthError as e:
        return templates.TemplateResponse(
            'error.html', {'error_message': e.error}
        )
    # Getting user info
    user = await oauth.discord.userinfo(token=token)
    if not user:
        return templates.TemplateResponse(
            'error.html', {'error_message': "Could not get user info!"}
        )
    user_dict = dict(user)

    # We save id in session
    save_user_session(request=request, user_id=int(user_dict['id']), provider=PROVIDER)

    user_schema = UserCreate(
        sso_id=int(user_dict['id']),
        sso_provider=PROVIDER,
        username=user_dict['username'],
        avatar_url=f"https://cdn.discordapp.com/avatars/{user_dict['id']}/{user_dict['avatar']}.png",
    )

    await crud_users.create_user_if_not_exist(session=session, user_schema=user_schema)
    
    return RedirectResponse(url='/home')


@router.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for("discord_auth")
    return await oauth.discord.authorize_redirect(request, redirect_uri)
