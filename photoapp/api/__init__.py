from fastapi import APIRouter

from api.users import router as users_router
from api.posts import router as posts_router
from api.auth import router as auth_router
from api.discord_sso import router as discord_sso_router
from api.github_sso import router as github_sso_router
from api.gallery import router as gallery_router
from api.upload import router as upload_router

router = APIRouter()

router.include_router(users_router)
router.include_router(posts_router)
router.include_router(auth_router)
router.include_router(discord_sso_router)
router.include_router(github_sso_router)
router.include_router(gallery_router)
router.include_router(upload_router)
