from fastapi import APIRouter

from app.core.database import check_database

router = APIRouter(tags=["health"])


@router.get("/")
def home():
    database_status = "ok" if check_database() else "unavailable"
    return {
        "message": "StockEdge API is running!",
        "database": database_status,
    }
