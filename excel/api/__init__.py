__all__ = ["router"]

from fastapi import APIRouter

from .v1 import router as v1_router

router = APIRouter(prefix="/excel")

router.include_router(router=v1_router, prefix="/api")
