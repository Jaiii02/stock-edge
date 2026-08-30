from fastapi import APIRouter, HTTPException

from app.services.stock_universe import get_symbols
from app.schemas.stocks import StockResponse
from services.peer_engine import get_stock_info


router = APIRouter(tags=["stocks"])


@router.get("/symbols", response_model=list[str])
def symbols():
    return get_symbols()


@router.get("/stocks/{symbol}", response_model=StockResponse)
def stock(symbol: str):
    result = get_stock_info(symbol.upper())
    if result is None:
        raise HTTPException(status_code=404, detail="Stock not found")
    return result
