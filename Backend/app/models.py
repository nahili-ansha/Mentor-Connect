from sqlalchemy import Table, Column, String, Text, ARRAY, MetaData, DateTime, ForeignKey
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

mentor_profiles = Table(
    "mentor_profiles",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id")),
    Column("bio", Text),
    Column("skills", ARRAY(Text)),
    Column("availability", Text),
    Column("created_at", DateTime, default=datetime.utcnow),
    Column("company", Text),
    Column("linkedin_url", Text),
    Column("timezone", Text),
    Column("categories", ARRAY(Text)),
)
    

