"""empty message

Revision ID: c9f71666811c
Revises: fdd6cf7610c2
Create Date: 2023-07-19 18:46:26.911934

"""
from alembic import op
import sqlalchemy as sa
import csv

from app.data import balance_movements, receiving_partner_balances

# revision identifiers, used by Alembic.
revision = 'c9f71666811c'
down_revision = 'fdd6cf7610c2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    with open("alembic/data/balance_movements.csv") as file:
        op.bulk_insert(balance_movements, list(csv.DictReader(file)))
    with open("alembic/data/balance_snapshots.csv") as file:
        op.bulk_insert(receiving_partner_balances, list(csv.DictReader(file)))


def downgrade() -> None:
    op.execute(receiving_partner_balances.delete())
    op.execute(balance_movements.delete())
