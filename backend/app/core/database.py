import os

from sqlalchemy import create_engine


# Read the connection string from the environment when one is provided.
# The default is useful for this local Docker-based development setup.
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://stockedge:stockedge_dev_password@localhost:5432/stockedge",
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)
