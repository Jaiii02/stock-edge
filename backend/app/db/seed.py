import csv

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import DATA_PATH
from app.core.database import engine
from app.db.models import Stock


def seed_stocks() -> int:
    """Copy unique symbols from the CSV into the stocks table."""
    with DATA_PATH.open(newline="", encoding="utf-8") as csv_file:
        symbols = {row["Symbol"].strip() for row in csv.DictReader(csv_file)}

    with Session(engine) as session:
        existing = set(session.scalars(select(Stock.symbol)))
        new_stocks = [Stock(symbol=symbol) for symbol in sorted(symbols - existing)]
        session.add_all(new_stocks)
        session.commit()

    return len(new_stocks)


if __name__ == "__main__":
    added = seed_stocks()
    print(f"added {added} stock symbols")
