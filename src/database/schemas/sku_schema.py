import time
from enum import Enum
from typing import Optional, List
from sqlalchemy import Column, ForeignKey, Enum as SQLAlchemyEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.sqltypes import JSON, String, Integer
from pydantic import BaseModel, validator
import uuid

from src.database.database_manager import Base
from src.database.schemas.vec3_schema import Vec3


class ShapeType(str, Enum):
    Unknown = "Unknown"
    Can = "Can"
    Bottle = "Bottle"
    Box = "Box"


class SkuSchema(Base):
    __tablename__ = "skus"

    jan_code = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    drink_size = Column(Integer, nullable=False)
    product_size = Column(JSON, nullable=False)
    shape_type = Column(SQLAlchemyEnum(ShapeType), nullable=False)
    image_url = Column(String, nullable=True)
    timestamp = Column(Integer, nullable=False, default=int(time.time()))
    brand_name = Column(String, ForeignKey("brands.name", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)


class Sku(BaseModel):
    jan_code: uuid.UUID
    name: str
    drink_size: int
    product_size: Vec3
    shape_type: ShapeType
    image_url: Optional[str] = None
    timestamp: int
    brand_name: str


class SkuList(BaseModel):
    brand_names: Optional[List[str]] = None


class SkuUpdate(BaseModel):
    name: str
    drink_size: int
    product_size: Vec3
    shape_type: ShapeType
    image_url: Optional[str] = None

    @validator('product_size', pre=True)
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


class SkuCreate(SkuUpdate):
    brand_name: str
