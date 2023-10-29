from typing import Optional

from fastapi import HTTPException, APIRouter
from uuid import UUID as PyUUID

from src.database.database_manager import SessionLocal
from src.database.schemas.brand_schema import BrandSchema
from src.database.schemas.sku_schema import Sku, SkuSchema, SkuCreate, SkuUpdate, SkuList

router = APIRouter()


@router.get("/skus", response_model=list[Sku])
def list_skus(request_data: Optional[SkuList] = None):
    brand_names = request_data.brand_names if request_data else None

    db = SessionLocal()
    if brand_names:
        skus = db.query(SkuSchema).filter(SkuSchema.brand_name.in_(brand_names)).all()
    else:
        skus = db.query(SkuSchema).all()
    db.close()
    return skus


@router.get("/skus/{jan_code}", response_model=Sku)
def get_sku(jan_code: PyUUID):
    db = SessionLocal()
    sku = db.query(SkuSchema).filter(SkuSchema.jan_code == jan_code).first()
    db.close()
    if sku is None:
        raise HTTPException(status_code=404, detail="Sku not found")
    return sku


@router.post("/skus", response_model=Sku)
def create_sku(sku: SkuCreate):
    db = SessionLocal()
    try:
        brand_ref = db.query(BrandSchema).filter(BrandSchema.name == sku.brand_name).first()
        if not brand_ref:
            raise HTTPException(status_code=404, detail=f"Unable to find Brand by name: {sku.brand_name}")

        db_sku = SkuSchema(**sku.model_dump())
        db.add(db_sku)
        db.commit()
        db.refresh(db_sku)
        return db_sku
    finally:
        db.close()


@router.put("/skus/{jan_code}", response_model=Sku)
def update_sku(jan_code: PyUUID, updated_sku: SkuUpdate):
    db = SessionLocal()
    try:
        existing_sku = db.query(SkuSchema).filter(SkuSchema.jan_code == jan_code).first()
        if existing_sku is None:
            raise HTTPException(status_code=404, detail="Sku not found")

        for attr, value in updated_sku.model_dump().items():
            setattr(existing_sku, attr, value)

        db.commit()
        db.refresh(existing_sku)
        return existing_sku
    finally:
        db.close()


@router.delete("/skus/{jan_code}", response_model=Sku)
def delete_sku(jan_code: PyUUID):
    db = SessionLocal()
    sku = db.query(SkuSchema).filter(SkuSchema.jan_code == jan_code).first()
    if sku is None:
        db.close()
        raise HTTPException(status_code=404, detail="Sku not found")
    db.delete(sku)
    db.commit()
    db.close()
    return sku
