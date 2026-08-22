"""Build stock comparison groups from the PostgreSQL stock universe."""
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import engine
from app.db.models import Stock

def get_stock_info(symbol : str) :
    with Session(engine) as session:
        stock = session.scalar(select(Stock).where(Stock.symbol == symbol))

        if stock is None:
            return None

        return {
            "symbol": stock.symbol,
            "company_name": stock.company_name,
            "industry": stock.industry,
        }


def get_peers(symbol : str) :
    with Session(engine) as session:
        stock = session.scalar(select(Stock).where(Stock.symbol == symbol))
        if stock is None:
            return None

        peer_query = (
            select(Stock.symbol)
            .where(Stock.industry == stock.industry, Stock.symbol != symbol)
            .order_by(Stock.symbol)
        )
        peer_symbols = list(session.scalars(peer_query))

        return {
            "company_name": stock.company_name,
            "industry": stock.industry,
            "peer_count": len(peer_symbols),
            "peer_symbols": peer_symbols,
        }












