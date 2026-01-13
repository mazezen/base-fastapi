from fastapi import APIRouter

from app.api import health, auth, user

router = APIRouter()

router.include_router(health.router, tags=['health'], prefix='/health')
router.include_router(auth.router, tags=["authentication"], prefix="/auth")
router.include_router(user.router, tags=["users"], prefix="/user")

