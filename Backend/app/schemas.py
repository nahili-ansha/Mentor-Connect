from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

# pydantic model for user data
class UserIn(BaseModel):
    email: str
    full_name: str
    role: str

# pydantic model for mentor input
class MentorIn(BaseModel):
    email: EmailStr
    full_name: str

# pydantic model for mentee input
class MenteeIn(BaseModel):
    email: EmailStr
    full_name: str

# pydantic model for user output
class UserOut(BaseModel):
    id: str
    email: str
    full_name: str
    role: str
    created_at: datetime

# pydantic model for mentor_profile
class MentorProfileIn(BaseModel):
    user_id: str
    bio: str
    skills: List[str]
    availability: str
    company: Optional[str] = None
    linkedin_url: Optional[str] = None
    timezone: Optional[str] = None
    categories: Optional[List[str]] = None

# pydantic model for mentor profile output
class MentorProfileOut(BaseModel):
    id: str
    user_id: str
    full_name: str
    email: str
    bio: str
    skills: List[str]
    availability: str
    created_at: datetime
    company: Optional[str] = None
    linkedin_url: Optional[str] = None
    timezone: Optional[str] = None
    categories: Optional[List[str]] = None


