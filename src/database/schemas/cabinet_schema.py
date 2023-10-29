from typing import List, Optional

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from pydantic import BaseModel, validator
import uuid

from sqlalchemy.sql.sqltypes import JSON

from src.database.database_manager import Base
from src.database.schemas.vec3_schema import Vec3


class CabinetSchema(Base):
    __tablename__ = "cabinets"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    store_id = Column(UUID(as_uuid=True), ForeignKey("stores.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    position = Column(JSON, nullable=False)
    size = Column(JSON, nullable=False)


class Cabinet(BaseModel):
    id: uuid.UUID
    position: Vec3
    size: Vec3
    store_id: uuid.UUID


class CabinetList(BaseModel):
    store_ids: Optional[List[uuid.UUID]] = None


class CabinetCreateUpdate(BaseModel):
    position: Vec3
    size: Vec3
    store_id: uuid.UUID

    @validator('position', 'size', pre=True)
    def validate_json_fields(cls, value):
        try:
            if not isinstance(value, dict):
                raise ValueError('Must be a dictionary')
            for key, val in value.items():
                if not isinstance(key, str) or not isinstance(val, (int, float)):
                    raise ValueError('Invalid data in dictionary')
            return value
        except Exception as e:
            raise ValueError('Invalid JSON data') from e
