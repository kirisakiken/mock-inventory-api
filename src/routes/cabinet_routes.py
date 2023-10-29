from fastapi import HTTPException, APIRouter
from uuid import UUID as PyUUID

from src.database.database_manager import SessionLocal
from src.database.schemas.cabinet_schema import Cabinet, CabinetSchema, CabinetCreateUpdate, CabinetList

router = APIRouter()


@router.get("/cabinets", response_model=list[Cabinet])
def list_cabinets(request_data: CabinetList):
    store_ids = request_data.store_ids

    db = SessionLocal()
    if store_ids:
        cabinets = db.query(CabinetSchema).filter(CabinetSchema.store_id.in_(store_ids)).all()
    else:
        cabinets = db.query(CabinetSchema).all()
    db.close()

    return cabinets


@router.get("/cabinets/{cabinet_id}", response_model=Cabinet)
def get_cabinet(cabinet_id: PyUUID):
    db = SessionLocal()
    cabinet = db.query(CabinetSchema).filter(CabinetSchema.id == cabinet_id).first()
    db.close()
    if cabinet is None:
        raise HTTPException(status_code=404, detail="Cabinet not found")
    return cabinet


@router.post("/cabinets", response_model=Cabinet)
def create_cabinet(cabinet: CabinetCreateUpdate):
    db = SessionLocal()
    try:
        db_cabinet = CabinetSchema(**cabinet.model_dump())
        db.add(db_cabinet)
        db.commit()
        db.refresh(db_cabinet)
        return db_cabinet
    finally:
        db.close()


@router.put("/cabinets/{cabinet_id}", response_model=Cabinet)
def update_cabinet(cabinet_id: PyUUID, updated_cabinet: CabinetCreateUpdate):
    db = SessionLocal()
    try:
        existing_cabinet = db.query(CabinetSchema).filter(CabinetSchema.id == cabinet_id).first()
        if existing_cabinet is None:
            raise HTTPException(status_code=404, detail="Cabinet not found")

        for attr, value in updated_cabinet.model_dump().items():
            setattr(existing_cabinet, attr, value)

        db.commit()
        db.refresh(existing_cabinet)
        return existing_cabinet
    finally:
        db.close()


@router.delete("/cabinets/{cabinet_id}", response_model=Cabinet)
def delete_cabinet(cabinet_id: PyUUID):
    db = SessionLocal()
    cabinet = db.query(CabinetSchema).filter(CabinetSchema.id == cabinet_id).first()
    if cabinet is None:
        db.close()
        raise HTTPException(status_code=404, detail="Cabinet not found")
    db.delete(cabinet)
    db.commit()
    db.close()
    return cabinet
