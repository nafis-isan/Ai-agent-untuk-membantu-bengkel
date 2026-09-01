"""Services API Endpoints"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.database import models
from app.database import schemas

router = APIRouter(prefix="/services", tags=["Services"])


@router.get("/", response_model=list[schemas.ServiceOrderResponse])
async def get_services(db: Session = Depends(get_db)):
    """Get all service orders"""
    return db.query(models.ServiceOrder).all()


@router.get("/{service_id}", response_model=schemas.ServiceOrderResponse)
async def get_service(service_id: int, db: Session = Depends(get_db)):
    """Get service by ID"""
    service = db.query(models.ServiceOrder).filter(models.ServiceOrder.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service tidak ditemukan")
    return service


@router.post("/", response_model=schemas.ServiceOrderResponse, status_code=201)
async def create_service(service: schemas.ServiceOrderCreate, db: Session = Depends(get_db)):
    """Create a new service order"""
    vehicle = db.query(models.Vehicle).filter(models.Vehicle.id == service.vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Kendaraan tidak ditemukan")

    if service.mechanic_id is not None:
        mechanic = db.query(models.Mechanic).filter(models.Mechanic.id == service.mechanic_id).first()
        if not mechanic:
            raise HTTPException(status_code=404, detail="Mechanic tidak ditemukan")

    db_service = models.ServiceOrder(**service.model_dump())
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service


@router.put("/{service_id}", response_model=schemas.ServiceOrderResponse)
async def update_service(service_id: int, service: schemas.ServiceOrderCreate, db: Session = Depends(get_db)):
    """Update service"""
    db_service = db.query(models.ServiceOrder).filter(models.ServiceOrder.id == service_id).first()
    if not db_service:
        raise HTTPException(status_code=404, detail="Service tidak ditemukan")

    db_service.vehicle_id = service.vehicle_id
    db_service.mechanic_id = service.mechanic_id
    db_service.complaint = service.complaint
    db_service.diagnosis = service.diagnosis
    db_service.status = service.status
    db_service.total_cost = service.total_cost

    db.commit()
    db.refresh(db_service)
    return db_service


@router.delete("/{service_id}")
async def delete_service(service_id: int, db: Session = Depends(get_db)):
    """Delete service"""
    db_service = db.query(models.ServiceOrder).filter(models.ServiceOrder.id == service_id).first()
    if not db_service:
        raise HTTPException(status_code=404, detail="Service tidak ditemukan")

    db.delete(db_service)
    db.commit()
    return {"status": "deleted"}
