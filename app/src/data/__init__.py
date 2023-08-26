import sqlalchemy
from sqlalchemy.sql import func
from sqlalchemy.sql.schema import UniqueConstraint

metadata = sqlalchemy.MetaData()

CURRENCY = sqlalchemy.Numeric(24, 8)
receiving_partner_balances = sqlalchemy.Table(
    "receiving_partner_balances",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.BigInteger, primary_key=True, nullable=False),
    sqlalchemy.Column("balance_id", sqlalchemy.BigInteger, nullable=False),
    sqlalchemy.Column("available_balance", CURRENCY, nullable=False),
    sqlalchemy.Column("balance_snapshot_date", sqlalchemy.DateTime, nullable=False),
    sqlalchemy.Column("creation_date", sqlalchemy.DateTime, server_default=func.now(), nullable=False),
    UniqueConstraint("balance_id", "balance_snapshot_date", name="unique_receiving_partner_balance"),
)

balance_movements = sqlalchemy.Table(
    "balance_movements",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.BigInteger, primary_key=True, nullable=False),
    sqlalchemy.Column("sending_partner_id", sqlalchemy.BigInteger, nullable=False, index=True),
    sqlalchemy.Column("receiving_partner_id", sqlalchemy.BigInteger, nullable=False, index=True),
    sqlalchemy.Column("balance_id", sqlalchemy.BigInteger, index=True, nullable=False),
    sqlalchemy.Column("balance_movement_amount", CURRENCY, nullable=False),
    sqlalchemy.Column("balance_movement_date", sqlalchemy.DateTime, nullable=False),
    UniqueConstraint(
        "sending_partner_id",
        "receiving_partner_id",
        "balance_movement_date",
        "balance_id",
        name="unique_balance_movement",
    ),
)
