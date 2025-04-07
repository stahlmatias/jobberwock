from pydantic import BaseModel
from typing import List, Optional

class JobCreate(BaseModel):
    title: str
    description: str
    company: str
    salary: int
    country: str
    skills: List[str]

class JobQuery(BaseModel):
    name: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    country: Optional[str] = None

class Job(JobCreate):
    id: int

