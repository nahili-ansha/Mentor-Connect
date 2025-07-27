from sqlalchemy import Table, Column, String, MetaData, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("email", String, unique=True,nullable=False ),
    Column("full_name", String),
    Column("role", String),
    Column("created_at", DateTime, default=datetime.utcnow)
)

