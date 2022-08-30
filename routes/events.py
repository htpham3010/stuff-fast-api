from fastapi import APIRouter, HTTPException, status, Depends
from models.events import Event, EventUpdate
from typing import List
from beanie import PydanticObjectId
from database.connection import Database
from auth.authenticate import authenticate

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
async def create_event(body: Event, user: str = Depends(authenticate)) -> dict:
    body.creator = user
    await event_db.save(body)

    return {"message": "Create successfully."}


@event_router.put("/{_id}}", response_model=Event)
async def update_event(
    _id: PydanticObjectId, body: EventUpdate, user: str = Depends(authenticate)
) -> Event:
    _event = await event_db.get(_id)

    if _event.creator != user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User not permission to update",
        )

    _update = await event_db.update(_id, body)

    if not _update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with id={id} ",
        )

    return _update


@event_router.delete("/{_id}")
async def delete_event(
    _id: PydanticObjectId, user: str = Depends(authenticate)
) -> dict:
    _event = await event_db.get(_id)

    if not _event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with id={_id} does not exist.",
        )

    if _event.creator != user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Current user not permission to delete",
        )

    result = await event_db.delete(_id)
    if not result:
        return {"message": "Delete failed"}

    return {"message": "Delete successfully!!!"}
