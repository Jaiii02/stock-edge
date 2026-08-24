"""Build stock comparison groups from the PostgreSQL stock universe."""
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import engine
from app.db.models import Company, Industry

def get_stock_info(symbol : str) :
    with Session(engine) as session:
        stock = session.scalar(select(Company).where(Company.symbol == symbol))

        if stock is None:
            return None

        return {
            "symbol": stock.symbol,
            "company_name": stock.company_name,
            "industry": session.get(Industry, stock.industry_id).name,
        }


def get_peers(symbol : str) :
    with Session(engine) as session:
        stock = session.scalar(select(Company).where(Company.symbol == symbol))
        if stock is None:
            return None

        industry = session.get(Industry, stock.industry_id)
        peer_query = select(Company.symbol).where(
            Company.industry_id == stock.industry_id,
            Company.symbol != symbol,
        ).order_by(Company.symbol)
        peer_symbols = list(session.scalars(peer_query))

        return {
            "company_name": stock.company_name,
            "industry": industry.name,
            "peer_count": len(peer_symbols),
            "peer_symbols": peer_symbols,
        }












