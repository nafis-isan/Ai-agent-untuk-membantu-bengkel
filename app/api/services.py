"""Services API Endpoints"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database import models, schemas

router = APIRouter(prefix="/api/services", tags=["services"])


@router.get("/")
async def get_services(db: Session = Depends(get_db)):
    """Get all services"""
    return db.query(models.Service).all()


@router.get("/{service_id}")
async def get_service(service_id: int, db: Session = Depends(get_db)):
    """Get service by ID"""
    return db.query(models.Service).filter(models.Service.id == service_id).first()


@router.post("/")
async def create_service(service: schemas.ServiceCreate, db: Session = Depends(get_db)):
    """Create a new service"""
    db_service = models.Service(**service.model_dump())
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service


@router.put("/{service_id}")
async def update_service(service_id: int, service: schemas.ServiceCreate, db: Session = Depends(get_db)):
    """Update service"""
    db_service = db.query(models.Service).filter(models.Service.id == service_id).first()
    if db_service:
        for key, value in service.model_dump().items():
            setattr(db_service, key, value)
        db.commit()
        db.refresh(db_service)
    return db_service


@router.delete("/{service_id}")
async def delete_service(service_id: int, db: Session = Depends(get_db)):
    """Delete service"""
    db_service = db.query(models.Service).filter(models.Service.id == service_id).first()
    if db_service:
        db.delete(db_service)
        db.commit()
    return {"status": "deleted"}
