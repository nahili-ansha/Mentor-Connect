from fastapi import FastAPI
from dotenv import load_dotenv
from databases import Database
import os

from pydantic import BaseModel
from sqlalchemy.sql import insert
from app.models import users, metadata
import uuid

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
database = Database(DATABASE_URL)

app = FastAPI()

@app.on_event("startup")
async def connect_db():
    await database.connect()

@app.on_event("shutdown")
async def disconnect_db():
    await database.disconnect()

# pydantic model for user data
class UserIn(BaseModel):
    email: str
    full_name: str
    role: str

@app.post("/users/")
async def create_user(user: UserIn):
    query = users.insert().values(
        id=uuid.uuid4(),
        email=user.email,
        full_name=user.full_name,
        role=user.role,
    )
    await database.execute(query)
    return {"status": "User created successfully!"}
