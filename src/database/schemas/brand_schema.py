from pydantic import BaseModel
from sqlalchemy import Column, String

from src.database.database_manager import Base


class BrandSchema(Base):
    __tablename__ = "brands"

    name = Column(String, primary_key=True, index=True)


class Brand(BaseModel):
    name: str


class BrandCreate(BaseModel):
    name: str

