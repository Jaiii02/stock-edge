import logging
import time
from datetime import datetime, timedelta, timezone
from typing import Any

import yfinance as yf
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import engine
from app.db.models import MarketDataSnapshot
from app.services.provider_errors import MarketDataUnavailableError

logger = logging.getLogger(__name__)


class MarketDataProvider:
    """Interface-like base class for providers of market data."""

    def get_stock_info(self, symbol: str) -> dict[str, Any]:
        raise NotImplementedError


class YahooFinanceProvider(MarketDataProvider):
    """Fetch company information from Yahoo Finance with limited retries."""

    def __init__(self, max_attempts: int = 3, retry_delay_seconds: float = 1.0, cache_hours: int = 24):
        self.max_attempts = max_attempts
        self.retry_delay_seconds = retry_delay_seconds
        self.cache_hours = cache_hours

    def get_stock_info(self, symbol: str) -> dict[str, Any]:
        ticker_symbol = f"{symbol.upper()}.NS"
        cached = self._get_recent_snapshot(symbol.upper())
        if cached is not None:
            logger.info("Using cached market data for %s", ticker_symbol)
            return cached

        for attempt in range(1, self.max_attempts + 1):
            try:
                logger.info("Fetching market data for %s (attempt %d/%d)", ticker_symbol, attempt, self.max_attempts)
                info = yf.Ticker(ticker_symbol).info
                if not isinstance(info, dict):
                    raise ValueError("Yahoo Finance returned an invalid response")
                self._save_snapshot(symbol.upper(), info)
                return info
            except Exception as exc:
                logger.warning("Market-data request failed for %s (attempt %d/%d)", ticker_symbol, attempt, self.max_attempts, exc_info=True)
                if attempt == self.max_attempts:
                    raise MarketDataUnavailableError(
                        f"Yahoo Finance unavailable for {ticker_symbol}"
                    ) from exc
                time.sleep(self.retry_delay_seconds)

    def _get_recent_snapshot(self, symbol: str) -> dict[str, Any] | None:
        cutoff = datetime.now(timezone.utc) - timedelta(hours=self.cache_hours)
        with Session(engine) as session:
            snapshot = session.scalar(
                select(MarketDataSnapshot)
                .where(
                    MarketDataSnapshot.symbol == symbol,
                    MarketDataSnapshot.source == "yahoo_finance",
                    MarketDataSnapshot.fetched_at >= cutoff,
                )
                .order_by(MarketDataSnapshot.fetched_at.desc())
            )
            return snapshot.payload if snapshot is not None else None

    def _save_snapshot(self, symbol: str, info: dict[str, Any]) -> None:
        with Session(engine) as session:
            session.add(
                MarketDataSnapshot(
                    symbol=symbol,
                    source="yahoo_finance",
                    fetched_at=datetime.now(timezone.utc),
                    payload=info,
                )
            )
            session.commit()


provider = YahooFinanceProvider()


def get_stock_info(symbol: str) -> dict[str, Any]:
    """Backward-compatible function used by the analysis pipeline."""
    return provider.get_stock_info(symbol)
