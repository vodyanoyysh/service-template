from fastapi import APIRouter

from serivce.api.edpoints.system import system_router

router = APIRouter()
router.include_router(system_router, tags=["system"])