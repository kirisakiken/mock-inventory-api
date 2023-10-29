from fastapi import HTTPException, APIRouter
from uuid import UUID as PyUUID

from src.database.database_manager import SessionLocal
from src.database.schemas.store_schema import Store, StoreSchema, StoreCreateUpdate, store_db_to_pydantic, \
    store_create_to_db

router = APIRouter()


@router.get("/stores", response_model=list[Store])
def list_stores():
    db = SessionLocal()
    stores = db.query(StoreSchema).all()
    db.close()
    return stores


@router.get("/stores/{store_id}", response_model=Store)
def get_store(store_id: PyUUID):
    db = SessionLocal()
    store = db.query(StoreSchema).filter(StoreSchema.id == store_id).first()
    db.close()
    if store is None:
        raise HTTPException(status_code=404, detail="Store not found")
    return store


@router.post("/stores", response_model=Store)
def create_store(store: StoreCreateUpdate):
    db = SessionLocal()
    try:
        db_store = StoreSchema(store_create_to_db(store))
        db.add(db_store)
        db.commit()
        db.refresh(db_store)
        return store_db_to_pydantic(db_store)
    finally:
        db.close()


@router.put("/stores/{store_id}", response_model=Store)
def update_store(store_id: PyUUID, updated_store: StoreCreateUpdate):
    db = SessionLocal()
    try:
        existing_store = db.query(StoreSchema).filter(StoreSchema.id == store_id).first()
        if existing_store is None:
            raise HTTPException(status_code=404, detail="Store not found")

        for attr, value in updated_store.model_dump().items():
            setattr(existing_store, attr, value)

        db.commit()
        db.refresh(existing_store)
        return store_db_to_pydantic(existing_store)
    finally:
        db.close()


@router.delete("/stores/{store_id}", response_model=Store)
def delete_store(store_id: PyUUID):
    db = SessionLocal()
    store = db.query(StoreSchema).filter(StoreSchema.id == store_id).first()
    if store is None:
        db.close()
        raise HTTPException(status_code=404, detail="Store not found")
    db.delete(store)
    db.commit()
    db.close()
    return store_db_to_pydantic(store)
