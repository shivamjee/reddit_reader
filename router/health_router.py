from fastapi import APIRouter
from pydantic import BaseModel

health_router = APIRouter()

class HealthResponse(BaseModel):
    status: str
    """
        Status okay response from the Health API
    """
@health_router.get("/", response_model=HealthResponse)
@health_router.get("/health", response_model=HealthResponse)
async def health():
    """
    Health check API which returns a json response of {"status": "ok"}.
    """
    return HealthResponse(status="ok")