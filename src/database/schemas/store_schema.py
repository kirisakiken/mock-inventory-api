from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from pydantic import BaseModel
import uuid

from src.database.database_manager import Base


class StoreSchema(Base):
    __tablename__ = "stores"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    brand = Column(String, ForeignKey("brands.name", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    name = Column(String)


class Store(BaseModel):
    id: uuid.UUID
    brand: str
    name: str


class StoreCreate(BaseModel):
    brand: str
    name: str


class StoreUpdate(BaseModel):
    name: str
