from fastapi import APIRouter, HTTPException

from src.database.database_manager import SessionLocal
from src.database.schemas.brand_schema import Brand, BrandSchema, BrandCreate

router = APIRouter()


@router.get("/brands", response_model=list[Brand])
def list_brands():
    db = SessionLocal()
    brands = db.query(BrandSchema).all()
    db.close()
    return brands


@router.post("/brands", response_model=Brand)
def create_brand(brand: BrandCreate):
    db = SessionLocal()
    try:
        name_conflict = db.query(BrandSchema).filter(BrandSchema.name == brand.name).first()
        if name_conflict:
            raise HTTPException(status_code=409, detail=f"Brand with name: {brand.name} already exists")

        db_brand = BrandSchema(**brand.model_dump())
        db.add(db_brand)
        db.commit()
        db.refresh(db_brand)
        return db_brand
    finally:
        db.close()


@router.delete("/brands/{brand_name}", response_model=Brand)
def delete_brand(brand_name: str):
    db = SessionLocal()
    brand = db.query(BrandSchema).filter(BrandSchema.name == brand_name).first()
    if brand is None:
        db.close()
        raise HTTPException(status_code=404, detail="Brand not found")
    db.delete(brand)
    db.commit()
    db.close()
    return brand
