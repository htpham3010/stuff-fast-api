from pydantic import BaseModel
from typing import List

class Event(BaseModel):
    id: int
    title: str
    image: str
    description: str
    tags: List[str]
    location: str

    class Config:
        schema_extra = {
            "example": {
                "title": "Power with FastAPI",
                "image":"",
                "description": "Learning FastAPI",
                "tags": ["python", "fastapi", "book","launch"],
                "location": "Microsoft Team"
            }
        }