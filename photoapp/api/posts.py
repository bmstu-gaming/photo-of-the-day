from fastapi import APIRouter


router = APIRouter(
    prefix="/posts",
    tags=["Users"],
)


# @router.get()