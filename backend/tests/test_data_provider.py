import pytest

from app.services.data_provider import YahooFinanceProvider
from app.services.provider_errors import MarketDataUnavailableError


class FakeTicker:
    def __init__(self, symbol, responses):
        self.symbol = symbol
        self.responses = responses

    @property
    def info(self):
        response = self.responses.pop(0)
        if isinstance(response, Exception):
            raise response
        return response


def test_provider_returns_cached_data_without_external_call(monkeypatch):
    provider = YahooFinanceProvider()
    cached = {"trailingPE": 15}
    monkeypatch.setattr(provider, "_get_recent_snapshot", lambda symbol: cached)
    monkeypatch.setattr("app.services.data_provider.yf.Ticker", lambda _: pytest.fail("Yahoo should not be called"))

    assert provider.get_stock_info("tcs") == cached


def test_provider_retries_then_succeeds(monkeypatch):
    responses = [ConnectionError("temporary"), ConnectionError("temporary"), {"trailingPE": 15}]
    monkeypatch.setattr("app.services.data_provider.yf.Ticker", lambda symbol: FakeTicker(symbol, responses))
    monkeypatch.setattr("app.services.data_provider.time.sleep", lambda _: None)
    provider = YahooFinanceProvider(max_attempts=3)
    monkeypatch.setattr(provider, "_get_recent_snapshot", lambda _: None)
    monkeypatch.setattr(provider, "_save_snapshot", lambda *_: None)

    assert provider.get_stock_info("tcs")["trailingPE"] == 15


def test_provider_raises_custom_error_after_final_failure(monkeypatch):
    responses = [ConnectionError("down")] * 3
    monkeypatch.setattr("app.services.data_provider.yf.Ticker", lambda symbol: FakeTicker(symbol, responses))
    monkeypatch.setattr("app.services.data_provider.time.sleep", lambda _: None)
    provider = YahooFinanceProvider(max_attempts=3)
    monkeypatch.setattr(provider, "_get_recent_snapshot", lambda _: None)

    with pytest.raises(MarketDataUnavailableError):
        provider.get_stock_info("tcs")


def test_expired_cache_falls_back_to_provider(monkeypatch):
    responses = [{"trailingPE": 15}]
    monkeypatch.setattr("app.services.data_provider.yf.Ticker", lambda symbol: FakeTicker(symbol, responses))
    monkeypatch.setattr("app.services.data_provider.time.sleep", lambda _: None)
    provider = YahooFinanceProvider()
    monkeypatch.setattr(provider, "_get_recent_snapshot", lambda _: None)
    saved = []
    monkeypatch.setattr(provider, "_save_snapshot", lambda symbol, info: saved.append((symbol, info)))

    result = provider.get_stock_info("tcs")

    assert result["trailingPE"] == 15
    assert saved == [("TCS", result)]
