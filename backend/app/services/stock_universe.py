from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import engine
from app.db.models import Company


def get_symbols() -> list[str]:
    """Return stock symbols stored in PostgreSQL."""
    with Session(engine) as session:
        query = select(Company.symbol).order_by(Company.symbol)
        return list(session.scalars(query))
