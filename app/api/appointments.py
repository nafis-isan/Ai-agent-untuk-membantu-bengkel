from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth import require_admin
from app.database import models, schemas
from app.database.dependencies import get_db

router = APIRouter(prefix="/appointments", tags=["Appointments"])


@router.get("/", response_model=list[schemas.AppointmentResponse])
def list_appointments(db: Session = Depends(get_db)):
    return db.query(models.Appointment).order_by(models.Appointment.scheduled_at.asc()).all()


@router.post("/", response_model=schemas.AppointmentResponse, status_code=201)
def create_appointment(
    appointment: schemas.AppointmentCreate,
    db: Session = Depends(get_db),
    admin: str = Depends(require_admin),
):
    if appointment.scheduled_at <= datetime.utcnow():
        raise HTTPException(status_code=422, detail="Waktu appointment harus di masa depan")
    if not db.query(models.Customer).filter(models.Customer.id == appointment.customer_id).first():
        raise HTTPException(status_code=404, detail="Pelanggan tidak ditemukan")
    if not db.query(models.Vehicle).filter(
        models.Vehicle.id == appointment.vehicle_id,
        models.Vehicle.customer_id == appointment.customer_id,
    ).first():
        raise HTTPException(status_code=404, detail="Kendaraan tidak ditemukan untuk pelanggan tersebut")
    item = models.Appointment(**appointment.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.patch("/{appointment_id}/status", response_model=schemas.AppointmentResponse)
def update_appointment_status(
    appointment_id: int,
    status: schemas.ServiceStatusUpdate,
    db: Session = Depends(get_db),
    admin: str = Depends(require_admin),
):
    item = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Appointment tidak ditemukan")
    if status.status not in {"scheduled", "confirmed", "cancelled", "completed"}:
        raise HTTPException(status_code=422, detail="Status appointment tidak valid")
    item.status = status.status
    db.commit()
    db.refresh(item)
    return item
