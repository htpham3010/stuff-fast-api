from pydantic import BaseModel
from typing import List, Optional
from sqlmodel import SQLModel, Field, Column, JSON


class Event(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    image: str
    description: str
    tags: List[str] = Field(sa_column=Column(JSON))
    location: str

    class Config:
        schema_extra = {
            "example": {
                "title": "Power with FastAPI",
                "image": "",
                "description": "Learning FastAPI",
                "tags": ["python", "fastAPI"],
                "location": "Microsoft Team",
            }
        }


class EventUpdate(SQLModel):
    title: Optional[str]
    image: Optional[str]
    description: Optional[str]
    tags: Optional[List[str]]
    location: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "title": "FastAPI stuff",
                "image": "",
                "description": "Learning FastAPI",
                "tags": ["python", "fastAPI"],
                "location": "Microsoft Team",
            }
        }
