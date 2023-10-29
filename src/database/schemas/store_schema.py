from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from pydantic import BaseModel
import uuid

from src.database.database_manager import Base


class StoreSchema(Base):
    __tablename__ = "stores"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    brand = Column(String, index=True)
    name = Column(String)


class Store(BaseModel):
    id: uuid.UUID
    brand: str
    name: str


class StoreCreateUpdate(BaseModel):
    brand: str
    name: str


def store_db_to_pydantic(store: StoreSchema):
    return Store(id=store.id, brand=store.brand, name=store.name)


def store_create_to_db(store: StoreCreateUpdate):
    return StoreSchema(**store.model_dump())
