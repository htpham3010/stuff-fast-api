from typing import Any, List, Optional

from beanie import PydanticObjectId, init_beanie
from models.events import Event
from models.users import User
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = None
    SECRET_KEY: Optional[str] = None

    async def initialize_database(self):
        client = AsyncIOMotorClient(self.DATABASE_URL)

        await init_beanie(
            database=client.get_default_database(),
            document_models=[Event, User],
        )

    class Config:
        env_file = ".env"


class Database:
    def __init__(self, model):
        self.model = model

    async def save(self, document) -> None:
        await document.create()
        return True

    async def get(self, _id: PydanticObjectId) -> Any:
        _doc = await self.model.get(_id)
        if not _doc:
            return False
        return _doc

    async def get_all(self) -> List[Any]:
        _docs = await self.model.find_all().to_list()

        return _docs

    async def update(self, _id: PydanticObjectId, _body: BaseModel) -> Any:
        _body = {_k: _v for _k, _v in _body.items() if _v is not None}
        _query = {"$set": {_field: _value for _field, _value in _body.items()}}

        _doc = await self.get(_id)

        if not _doc:
            return False

        await _doc.update(_query)
        return _doc

    async def delete(self, _id: PydanticObjectId) -> bool:
        _doc = await self.get(_id)

        if not _doc:
            return False

        await _doc.delete()
        return True
