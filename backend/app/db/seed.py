import csv

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import DATA_PATH
from app.core.database import engine
from app.db.models import Company, Industry


def seed_stocks() -> int:
    """Copy unique symbols from the CSV into the stocks table."""
    with DATA_PATH.open(newline="", encoding="utf-8") as csv_file:
        rows = list(csv.DictReader(csv_file))

    with Session(engine) as session:
        industries = {item.name: item for item in session.scalars(select(Industry))}
        companies = {item.symbol: item for item in session.scalars(select(Company))}

        new_stocks = []
        for row in rows:
            symbol = row["Symbol"].strip()
            company_name = row["Company Name"].strip()
            industry = row["Industry"].strip()

            industry_record = industries.get(industry)
            if industry_record is None:
                industry_record = Industry(name=industry)
                session.add(industry_record)
                session.flush()
                industries[industry] = industry_record

            if symbol in companies:
                companies[symbol].company_name = company_name
                companies[symbol].industry_id = industry_record.id
            else:
                new_stocks.append(
                    Company(
                        symbol=symbol,
                        company_name=company_name,
                        industry_id=industry_record.id,
                    )
                )

        session.add_all(new_stocks)
        session.commit()

    return len(new_stocks)


if __name__ == "__main__":
    added = seed_stocks()
    print(f"added {added} stock symbols")
