from fastapi import APIRouter, Body, HTTPException, status
from models.events import Event
from typing import List
from beanie import PydanticObjectId
from database.connection import Database

event_router = APIRouter(tags=["Events"])

event_db = Database(Event)


@event_router.get("/", response_model=List[Event])
async def retrieve_all_events() -> List[Event]:
    _events = await event_db.get_all()

    return _events


@event_router.get("/{_id}", response_model=Event)
async def retrieve_event(_id: PydanticObjectId) -> Event:
    _event = await event_db.get(_id)

    if not _event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with id={id} does not exists",
        )
    return _event


@event_router.post("/")
async def create_event(body: Event = Body(...)) -> dict:
    await event_db.save(body)

    return {"message": "Create successfully."}


@event_router.delete("/{_id}")
async def delete_event(_id: PydanticObjectId) -> dict:
    _event = await event_db.delete(_id)

    if not _event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with id={id} does not exist.",
        )
    return {"message": "Delete successfully!!!"}
