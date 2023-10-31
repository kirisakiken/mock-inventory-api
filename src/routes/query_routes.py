from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException

from src.database.database_manager import SessionLocal
from src.database.schemas.brand_schema import BrandSchema
from src.database.schemas.cabinet_schema import CabinetSchema, Cabinet
from src.database.schemas.lane_schema import LaneSchema, Lane
from src.database.schemas.query_schema import StoreInfo, BrandInfo
from src.database.schemas.row_schema import RowSchema, Row
from src.database.schemas.sku_schema import Sku, SkuSchema
from src.database.schemas.store_schema import StoreSchema

router = APIRouter()


@router.get("/query/stores/{store_id}", response_model=StoreInfo)
def query_store(store_id: UUID):
    db = SessionLocal()
    store = db.query(StoreSchema).filter(StoreSchema.id == store_id).first()
    if not store:
        raise HTTPException(status_code=404, detail=f"Unable to find store by id: {store_id}")
    cabinets: List[Cabinet] = db.query(CabinetSchema).filter(CabinetSchema.store_id == store_id).all()
    rows: List[Row] = []
    lanes: List[Lane] = []

    for cabinet in cabinets:
        rows.extend(db.query(RowSchema).filter(RowSchema.cabinet_id == cabinet.id).all())

    for row in rows:
        lanes.extend(db.query(LaneSchema).filter(LaneSchema.row_id == row.id).all())

    db.close()

    return StoreInfo(store=store, cabinets=cabinets, rows=rows, lanes=lanes)


@router.get("/query/brands/{brand_name}", response_model=BrandInfo)
def query_brand(brand_name: str):
    db = SessionLocal()
    brand = db.query(BrandSchema).filter(BrandSchema.name == brand_name).first()
    if not brand:
        raise HTTPException(status_code=404, detail=f"Unable to find Brand by name: {brand_name}")

    skus: List[Sku] = db.query(SkuSchema).filter(SkuSchema.brand_name == brand_name).all()

    db.close()

    return BrandInfo(brand=brand, skus=skus)
