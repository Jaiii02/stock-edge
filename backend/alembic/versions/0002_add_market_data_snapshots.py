"""add market data snapshots"""
from alembic import op
import sqlalchemy as sa

revision = "0002_market_data_snapshots"
down_revision = "0001_companies_industries"
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        "market_data_snapshots",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("symbol", sa.String(20), nullable=False),
        sa.Column("source", sa.String(50), nullable=False),
        sa.Column("fetched_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("as_of_date", sa.Date(), nullable=True),
        sa.Column("payload", sa.JSON(), nullable=False),
    )
    op.create_index("ix_market_data_snapshots_symbol", "market_data_snapshots", ["symbol"])
    op.create_index("ix_market_data_snapshots_source", "market_data_snapshots", ["source"])
    op.create_index("ix_market_data_snapshots_fetched_at", "market_data_snapshots", ["fetched_at"])

def downgrade():
    op.drop_index("ix_market_data_snapshots_fetched_at", table_name="market_data_snapshots")
    op.drop_index("ix_market_data_snapshots_source", table_name="market_data_snapshots")
    op.drop_index("ix_market_data_snapshots_symbol", table_name="market_data_snapshots")
    op.drop_table("market_data_snapshots")
