__all__ = ["router"]


from fastapi import APIRouter

from .handles import router as excel_router


router = APIRouter(prefix="/v1")

router.include_router(router=excel_router)
