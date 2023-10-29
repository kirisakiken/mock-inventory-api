import uuid
from typing import Optional, List

from pydantic import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, Float
from sqlalchemy.dialects.postgresql import UUID

from src.database.database_manager import Base


class LaneSchema(Base):
    __tablename__ = "lanes"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    jan_code = Column(UUID, ForeignKey("skus.jan_code", ondelete="SET NULL", onupdate="SET NULL"), nullable=True)
    quantity = Column(Integer, nullable=False, default=0)
    position_x = Column(Float, nullable=False, default=0)
    row_id = Column(UUID, ForeignKey("rows.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)


class Lane(BaseModel):
    id: uuid.UUID
    jan_code: Optional[uuid.UUID]
    quantity: int
    position_x: float
    row_id: uuid.UUID


class LaneList(BaseModel):
    row_ids: Optional[List[str]] = None


class LaneUpdate(BaseModel):
    jan_code: Optional[str] = None
    quantity: int
    position_x: float


class LaneCreate(LaneUpdate):
    row_id: str
