from fastapi import APIRouter

from analyzer import analyze_stock


router = APIRouter(tags=["analysis"])


@router.get("/analyze/{symbol}")
def analyze(symbol: str):
    return analyze_stock(symbol.upper())
