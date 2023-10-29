from typing import Optional, List

from sqlalchemy import Column, ForeignKey, Float
from sqlalchemy.dialects.postgresql import UUID
from pydantic import BaseModel
import uuid
from src.database.database_manager import Base


class RowSchema(Base):
    __tablename__ = "rows"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    position_z = Column(Float, nullable=False, default=0)
    height_z = Column(Float, nullable=False, default=0)
    cabinet_id = Column(UUID(as_uuid=True), ForeignKey("cabinets.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)


class Row(BaseModel):
    id: uuid.UUID
    position_z: float
    height_z: float
    cabinet_id: uuid.UUID


class RowList(BaseModel):
    cabinet_ids: Optional[List[uuid.UUID]] = None


class RowUpdate(BaseModel):
    position_z: Optional[float] = 0
    height_z: Optional[float] = 0


class RowCreate(RowUpdate):
    cabinet_id: uuid.UUID
