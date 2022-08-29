from fastapi import (
    APIRouter,
    Body,
    HTTPException,
    status,
    Depends,
    Request,
    status,
)
from database.connection import get_session
from models.events import Event, EventUpdate
from typing import List
from sqlmodel import select

event_router = APIRouter(tags=["Events"])

events = []


@event_router.get("/", response_model=List[Event])
async def retrieve_all_events(session=Depends(get_session)) -> List[Event]:
    _qr = select(Event)
    events = session.exec(_qr).all()
    return events


@event_router.get("/{id}", response_model=Event)
async def retrieve_event(id: int, session=Depends(get_session)) -> Event:
    event = session.get(Event, id)

    if event:
        return event

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Event not found"
    )


@event_router.post("/")
async def create_event(event: Event, session=Depends(get_session)):
    session.add(event)
    try:
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Occur error!!!"
        )
    finally:
        session.refresh(event)

    return {"message": "Create successfully."}


@event_router.put("/{id}", response_model=Event)
async def update_event(
    id: int, _update: EventUpdate, session=Depends(get_session)
):
    _event = session.get(Event, id)
    if _event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with id={id} not found",
        )

    _data = _update.dict(exclude_unset=True)
    for _k, _v in _data.items():
        setattr(_event, _k, _v)

    session.add(_event)
    try:
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Occur error!!!"
        )
    finally:
        session.refresh(_event)

    return _event


@event_router.delete("/{id}")
async def delete_event(id: int, session=Depends(get_session)) -> dict:

    _event = session.get(Event, id)

    if _event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with id={id} not found",
        )

    session.delete(_event)
    try:
        session.commit()
    except Exception as e:
        print(e)
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Occur error!!!"
        )
    return {"message": "Delete successfully"}
