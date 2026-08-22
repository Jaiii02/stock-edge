import csv

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import DATA_PATH
from app.core.database import engine
from app.db.models import Stock


def seed_stocks() -> int:
    """Copy unique symbols from the CSV into the stocks table."""
    with DATA_PATH.open(newline="", encoding="utf-8") as csv_file:
        rows = list(csv.DictReader(csv_file))

    with Session(engine) as session:
        existing = {
            stock.symbol: stock
            for stock in session.scalars(select(Stock))
        }

        new_stocks = []
        for row in rows:
            symbol = row["Symbol"].strip()
            company_name = row["Company Name"].strip()
            industry = row["Industry"].strip()

            if symbol in existing:
                existing[symbol].company_name = company_name
                existing[symbol].industry = industry
            else:
                new_stocks.append(
                    Stock(
                        symbol=symbol,
                        company_name=company_name,
                        industry=industry,
                    )
                )

        session.add_all(new_stocks)
        session.commit()

    return len(new_stocks)


if __name__ == "__main__":
    added = seed_stocks()
    print(f"added {added} stock symbols")
