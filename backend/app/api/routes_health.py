from fastapi import APIRouter

from app.core.database import check_database
from app.schemas.health import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/", response_model=HealthResponse)
@router.get("/health", response_model=HealthResponse)
def home():
    database_status = "ok" if check_database() else "unavailable"
    return {
        "message": "StockEdge API is running!",
        "database": database_status,
    }
