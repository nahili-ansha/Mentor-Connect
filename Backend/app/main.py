from fastapi import FastAPI
from dotenv import load_dotenv
from databases import Database
import os

from app.schemas import UserIn, MentorIn, MenteeIn, UserOut
from sqlalchemy.sql import insert
from app.models import users, metadata
import uuid

from typing import List
from datetime import datetime
from sqlalchemy import select


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

@app.post("/users/")
async def create_user(user: UserIn):
    query = users.insert().values(
        id=uuid.uuid4(),
        email=user.email,
        full_name=user.full_name,
        role=user.role,
        created_at=datetime.utcnow()
    )
    await database.execute(query)
    return {"status": "User created successfully!"}


@app.post("/mentors/")
async def create_mentor(mentor: MentorIn):
    query = users.insert().values(
        id=uuid.uuid4(),
        email=mentor.email,
        full_name=mentor.full_name,
        role="mentor",
        created_at=datetime.utcnow()
    )
    await database.execute(query)
    return {"status": "mentor created successfully!"}


@app.post("/mentees/")
async def create_mentee(mentee: MenteeIn):
    query = users.insert().values(
        id=uuid.uuid4(),
        email=mentee.email,
        full_name=mentee.full_name,
        role="mentee",
        created_at = datetime.utcnow()
    )
    await database.execute(query)
    return {"status": "mentee created successfully!"}


@app.get("/mentors/",response_model=List[UserOut] )
async def get_mentors():
    query = select(users).where(users.c.role == "mentor")
    results = await database.fetch_all(query)
    return [
        {
            "id": str(row["id"]),
            "email": row["email"],
            "full_name": row["full_name"],
            "role": row["role"],
            "created_at": row["created_at"] or datetime.utcnow()
        }
        for row in results
    ]

@app.get("/users", response_model=List[UserOut])
async def get_users():
    query = users.select()
    results = await database.fetch_all(query)
    return [
        {
            "id": str(row["id"]),
            "email": row["email"],
            "full_name": row["full_name"],
            "role": row["role"],
            "created_at": row["created_at"] or datetime.utcnow()
        }
        for row in results
    ]

@app.get("/mentees/", response_model=List[UserOut])
async def get_mentees():
    query = select(users).where(users.c.role == "mentee")
    results = await database.fetch_all(query)
    return [
        {
            "id": str(row["id"]),
            "email": row["email"],
            "full_name": row["full_name"],
            "role": row["role"],
            "created_at": row["created_at"] or datetime.utcnow()
        }
        for row in results
    ]