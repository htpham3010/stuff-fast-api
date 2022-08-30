from pydantic import BaseModel
from typing import List, Optional
from beanie import Document


class Event(Document):
    creator: Optional[str]
    title: str
    image: str
    description: str
    tags: List[str]
    location: str

    class Config:
        schema_extra = {
            "example": {
                "title": "Power with FastAPI",
                "image": "stuff-image.png",
                "description": "Learning FastAPI",
                "tags": ["python", "fastapi"],
                "location": "Microsoft Team",
            }
        }

    class Settings:
        name = "events"


class EventUpdate(BaseModel):
    title: Optional[str]
    image: Optional[str]
    description: Optional[str]
    tags: Optional[List[str]]
    location: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "title": "Stuff FastApi",
                "image": "stuff-image.png",
                "description": "Stuff Learning FastAPI",
                "tags": ["python", "fastapi"],
                "location": "Microsoft Team",
            }
        }
