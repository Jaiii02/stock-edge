from fastapi import APIRouter

from app.services.stock_universe import get_symbols


router = APIRouter(tags=["stocks"])


@router.get("/symbols")
def symbols():
    return get_symbols()
