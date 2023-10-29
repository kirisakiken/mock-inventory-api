from typing import Optional

from fastapi import APIRouter, HTTPException
from uuid import UUID as PyUUID

from src.database.database_manager import SessionLocal
from src.database.schemas.lane_schema import LaneList, LaneSchema, Lane, LaneCreate, LaneUpdate
from src.database.schemas.row_schema import RowSchema
from src.database.schemas.sku_schema import SkuSchema

router = APIRouter()


@router.get("/lanes", response_model=list[Lane])
def list_lanes(request_data: Optional[LaneList] = None):
    row_ids = request_data.row_ids if request_data else None

    db = SessionLocal()
    if row_ids:
        lanes = db.query(LaneSchema).filter(LaneSchema.row_id.in_(row_ids)).all()
    else:
        lanes = db.query(LaneSchema).all()
    db.close()
    return lanes


@router.get("/lanes/{lane_id}", response_model=Lane)
def get_lane(lane_id: PyUUID):
    db = SessionLocal()
    lane = db.query(LaneSchema).filter(LaneSchema.id == lane_id).first()
    if not lane:
        raise HTTPException(status_code=404, detail=f"Unable to find lane by id: {lane_id}")
    return lane


@router.post("/lanes", response_model=Lane)
def create_lane(lane: LaneCreate):
    db = SessionLocal()
    try:
        row_ref = db.query(RowSchema).filter(RowSchema.id == lane.row_id).first()
        if not row_ref:
            raise HTTPException(status_code=404, detail=f"Unable to find row by id: {lane.row_id}")
        if lane.jan_code:
            sku_ref = db.query(SkuSchema).filter(SkuSchema.jan_code == lane.jan_code).first()
            if not sku_ref:
                raise HTTPException(status_code=404, detail=f"Unable to find sku by jan_code: {lane.jan_code}")

        db_lane = LaneSchema(**lane.model_dump())
        db.add(db_lane)
        db.commit()
        db.refresh(db_lane)
        return db_lane
    finally:
        db.close()


@router.put("/lanes/{lane_id}", response_model=Lane)
def update_lane(lane_id: PyUUID, updated_lane: LaneUpdate):
    db = SessionLocal()
    try:
        existing_lane = db.query(LaneSchema).filter(LaneSchema.id == lane_id).first()
        if not existing_lane:
            raise HTTPException(status_code=404, detail=f"Unable to find lane by id: {lane_id}")

        for attr, value in updated_lane.model_dump().items():
            setattr(existing_lane, attr, value)

        db.commit()
        db.refresh(existing_lane)
        return existing_lane
    finally:
        db.close()


@router.delete("/lanes/{lane_id}", response_model=Lane)
def delete_lane(lane_id: PyUUID):
    db = SessionLocal()
    lane = db.query(LaneSchema).filter(LaneSchema.id == lane_id).first()
    if not lane:
        db.close()
        raise HTTPException(status_code=404, detail=f"Unable to find lane by id: {lane_id}")
    db.delete(lane)
    db.commit()
    db.close()
    return lane
