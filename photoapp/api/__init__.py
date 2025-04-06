from fastapi import APIRouter

from api.home import router as home_router
from api.users import router as users_router
from api.posts import router as posts_router
from api.discord_sso import router as discord_sso_router

router = APIRouter()

router.include_router(users_router)
router.include_router(posts_router)
router.include_router(home_router)
router.include_router(discord_sso_router)