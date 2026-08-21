from app.core.database import engine
from app.db.base import Base
from app.db import models  # noqa: F401 - registers models with Base.metadata


def initialize_database() -> None:
    """Create tables that do not exist yet."""
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    initialize_database()
    print("database tables initialized")
