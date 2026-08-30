from fastapi import APIRouter, HTTPException

from analyzer import analyze_stock
from app.schemas.analysis import AnalysisResponse


router = APIRouter(tags=["analysis"])


@router.get("/analyze/{symbol}", response_model=AnalysisResponse)
def analyze(symbol: str):
    try:
        result = analyze_stock(symbol.upper())
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Market data is temporarily unavailable") from exc
    if isinstance(result, dict) and result.get("error") == "Stock not found":
        raise HTTPException(status_code=404, detail="Stock not found")
    return result
