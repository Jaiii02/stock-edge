import logging
import time
from typing import Any

import yfinance as yf

from app.services.provider_errors import MarketDataUnavailableError

logger = logging.getLogger(__name__)


class MarketDataProvider:
    """Interface-like base class for providers of market data."""

    def get_stock_info(self, symbol: str) -> dict[str, Any]:
        raise NotImplementedError


class YahooFinanceProvider(MarketDataProvider):
    """Fetch company information from Yahoo Finance with limited retries."""

    def __init__(self, max_attempts: int = 3, retry_delay_seconds: float = 1.0):
        self.max_attempts = max_attempts
        self.retry_delay_seconds = retry_delay_seconds

    def get_stock_info(self, symbol: str) -> dict[str, Any]:
        ticker_symbol = f"{symbol.upper()}.NS"
        for attempt in range(1, self.max_attempts + 1):
            try:
                logger.info("Fetching market data for %s (attempt %d/%d)", ticker_symbol, attempt, self.max_attempts)
                info = yf.Ticker(ticker_symbol).info
                if not isinstance(info, dict):
                    raise ValueError("Yahoo Finance returned an invalid response")
                return info
            except Exception as exc:
                logger.warning("Market-data request failed for %s (attempt %d/%d)", ticker_symbol, attempt, self.max_attempts, exc_info=True)
                if attempt == self.max_attempts:
                    raise MarketDataUnavailableError(
                        f"Yahoo Finance unavailable for {ticker_symbol}"
                    ) from exc
                time.sleep(self.retry_delay_seconds)


provider = YahooFinanceProvider()


def get_stock_info(symbol: str) -> dict[str, Any]:
    """Backward-compatible function used by the analysis pipeline."""
    return provider.get_stock_info(symbol)
