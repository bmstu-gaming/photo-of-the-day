from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse


router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)


@router.get("/logout")
async def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url='/gallery')


# Save user id in session after successfull SSO auth
def save_user_session(request: Request, user_id: int, provider: str) -> None:
    request.session['user'] = {
        'id': user_id,
        'provider': provider
    }
