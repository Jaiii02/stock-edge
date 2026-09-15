import pytest
from fastapi import HTTPException

from app.api import routes_analysis, routes_stocks
from app.services.provider_errors import MarketDataUnavailableError


def test_stock_route_returns_404_for_unknown_symbol(monkeypatch):
    monkeypatch.setattr(routes_stocks, "get_stock_info", lambda _: None)

    with pytest.raises(HTTPException) as error:
        routes_stocks.stock("unknown")

    assert error.value.status_code == 404


def test_analysis_route_returns_404_for_unknown_symbol(monkeypatch):
    monkeypatch.setattr(routes_analysis, "analyze_stock", lambda _: {"error": "Stock not found"})

    with pytest.raises(HTTPException) as error:
        routes_analysis.analyze("unknown")

    assert error.value.status_code == 404


def test_analysis_route_returns_503_for_provider_failure(monkeypatch):
    def fail(_):
        raise MarketDataUnavailableError("provider unavailable")

    monkeypatch.setattr(routes_analysis, "analyze_stock", fail)

    with pytest.raises(HTTPException) as error:
        routes_analysis.analyze("TCS")

    assert error.value.status_code == 503


def test_successful_stock_lookup_returns_response(monkeypatch):
    monkeypatch.setattr(
        routes_stocks,
        "get_stock_info",
        lambda symbol: {"symbol": symbol, "company_name": "Example Ltd", "industry": "Technology"},
    )

    assert routes_stocks.stock("tcs")["symbol"] == "TCS"


def test_successful_analysis_returns_result(monkeypatch):
    result = {
        "symbol": "TCS",
        "scoring_model_version": "business-quality-v1",
        "overall_score": 7.5,
        "recommendation": "Buy",
        "overall_confidence": {"score": 90, "level": "High"},
        "business_quality": {},
        "valuation": {},
        "strengths": [],
        "weaknesses": [],
        "warnings": [],
    }
    monkeypatch.setattr(routes_analysis, "analyze_stock", lambda _: result)

    assert routes_analysis.analyze("tcs")["recommendation"] == "Buy"
