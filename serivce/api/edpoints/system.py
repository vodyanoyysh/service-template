import prometheus_client
from fastapi import APIRouter, Response

system_router = APIRouter()


@system_router.get("/health", summary="Получить health check")
async def health_check():
    return {
        "status": "UP",
        "detail": {}
    }


@system_router.get("/metrics", summary="Получить метрики")
async def metrics():
    return Response(content=prometheus_client.generate_latest(), media_type="text/plain")
