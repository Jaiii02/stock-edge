"""add normalized company and industry tables"""
from alembic import op
import sqlalchemy as sa

revision = "0001_companies_industries"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table("industries", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("name", sa.String(100), nullable=False, unique=True))
    op.create_index("ix_industries_name", "industries", ["name"], unique=True)
    op.create_table("companies", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("symbol", sa.String(20), nullable=False, unique=True), sa.Column("company_name", sa.String(200)), sa.Column("industry_id", sa.Integer(), sa.ForeignKey("industries.id"), nullable=False))
    op.create_index("ix_companies_symbol", "companies", ["symbol"], unique=True)
    op.create_index("ix_companies_industry_id", "companies", ["industry_id"])

def downgrade():
    op.drop_index("ix_companies_industry_id", table_name="companies")
    op.drop_index("ix_companies_symbol", table_name="companies")
    op.drop_table("companies")
    op.drop_index("ix_industries_name", table_name="industries")
    op.drop_table("industries")
