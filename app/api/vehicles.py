"""Vehicles API Endpoints"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database import models, schemas

router = APIRouter(prefix="/api/vehicles", tags=["vehicles"])


@router.get("/")
async def get_vehicles(db: Session = Depends(get_db)):
    """Get all vehicles"""
    return db.query(models.Vehicle).all()


@router.get("/{vehicle_id}")
async def get_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    """Get vehicle by ID"""
    return db.query(models.Vehicle).filter(models.Vehicle.id == vehicle_id).first()


@router.post("/")
async def create_vehicle(vehicle: schemas.VehicleCreate, db: Session = Depends(get_db)):
    """Create a new vehicle"""
    db_vehicle = models.Vehicle(**vehicle.model_dump())
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle


@router.put("/{vehicle_id}")
async def update_vehicle(vehicle_id: int, vehicle: schemas.VehicleCreate, db: Session = Depends(get_db)):
    """Update vehicle"""
    db_vehicle = db.query(models.Vehicle).filter(models.Vehicle.id == vehicle_id).first()
    if db_vehicle:
        for key, value in vehicle.model_dump().items():
            setattr(db_vehicle, key, value)
        db.commit()
        db.refresh(db_vehicle)
    return db_vehicle


@router.delete("/{vehicle_id}")
async def delete_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    """Delete vehicle"""
    db_vehicle = db.query(models.Vehicle).filter(models.Vehicle.id == vehicle_id).first()
    if db_vehicle:
        db.delete(db_vehicle)
        db.commit()
    return {"status": "deleted"}
