from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Depends
from app.auth import get_current_user
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
from databases import Database
import os

from app.schemas import UserIn, MentorIn, MenteeIn, UserOut, MentorProfileIn, MentorProfileOut
from sqlalchemy.sql import insert
from app.models import users, mentor_profiles, metadata
import uuid

from typing import List
from datetime import datetime
from sqlalchemy import select, join


DATABASE_URL = os.getenv("DATABASE_URL")
print("Database URL:", DATABASE_URL)  # Debugging line to check if the URL is loaded correctly
database = Database(DATABASE_URL)

app = FastAPI()

@app.on_event("startup")
async def connect_db():
    await database.connect()

@app.on_event("shutdown")
async def disconnect_db():
    await database.disconnect()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Create user (protected)
@app.post("/users/")
async def create_user(user: UserIn, current_user = Depends(get_current_user)):
    query = users.insert().values(
        id=uuid.uuid4(),
        email=user.email,
        full_name=user.full_name,
        role=user.role,
        created_at=datetime.utcnow()
    )
    await database.execute(query)
    return {"status": "User created successfully!"}

# Create mentor (protected)
@app.post("/mentors/")
async def create_mentor(mentor: MentorIn, current_user = Depends(get_current_user)):
    query = users.insert().values(
        id=uuid.uuid4(),
        email=mentor.email,
        full_name=mentor.full_name,
        role="mentor",
        created_at=datetime.utcnow()
    )
    await database.execute(query)
    return {"status": "mentor created successfully!"}

# Create mentee (protected)
@app.post("/mentees/")
async def create_mentee(mentee: MenteeIn, current_user = Depends(get_current_user)):
    query = users.insert().values(
        id=uuid.uuid4(),
        email=mentee.email,
        full_name=mentee.full_name,
        role="mentee",
        created_at = datetime.utcnow()
    )
    await database.execute(query)
    return {"status": "mentee created successfully!"}

# Create mentor profile (protected)
@app.post("/mentor_profiles/")
async def create_mentor_profile(profile: MentorProfileIn, current_user = Depends(get_current_user)):
    query = insert(mentor_profiles).values(
        id=uuid.uuid4(),
        user_id=profile.user_id,
        bio=profile.bio,
        skills=profile.skills,
        availability=profile.availability,
        created_at=datetime.utcnow(),
        company=profile.company,
        linkedin_url=profile.linkedin_url,
        timezone=profile.timezone,
        categories=profile.categories
    )
    await database.execute(query)
    return {"status": "mentor profile created successfully!"}

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

@app.get("/mentor_profiles/", response_model = List[MentorProfileOut])
async def get_mentor_profiles():
    try:
        j = join(mentor_profiles, users, mentor_profiles.c.user_id == users.c.id)
        query = select(
            mentor_profiles.c.id,
            mentor_profiles.c.user_id,
            users.c.full_name,
            users.c.email,
            mentor_profiles.c.bio,
            mentor_profiles.c.skills,
            mentor_profiles.c.availability,
            mentor_profiles.c.created_at,
            mentor_profiles.c.company,
            mentor_profiles.c.linkedin_url,
            mentor_profiles.c.timezone,
            mentor_profiles.c.categories
        ).select_from(j)

        rows = await database.fetch_all(query)
        return [
            {
                "id": str(row["id"]),
                "user_id": str(row["user_id"]),
                "full_name": row["full_name"],
                "email": row["email"],
                "bio": row["bio"],
                "skills": row["skills"],
                "availability": row["availability"],
                "created_at": row["created_at"] or datetime.utcnow(),
                "company": row["company"],
                "linkedin_url": row["linkedin_url"],
                "timezone": row["timezone"],
                "categories": row["categories"]
            }
            for row in rows
        ]
    except Exception as e:
         raise HTTPException(status_code=500, detail=str(e))

