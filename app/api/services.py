"""Services API Endpoints"""

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.database import models
from app.database import schemas
from app.auth import require_admin

router = APIRouter(prefix="/services", tags=["Services"])

STATUS_TRANSITIONS = {
    "draft": {"waiting", "scheduled", "cancelled"},
    "scheduled": {"waiting", "cancelled"},
    "waiting": {"in_progress", "cancelled"},
    "in_progress": {"completed", "cancelled"},
    "completed": set(),
    "cancelled": set(),
}


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
async def create_service(
    service: schemas.ServiceOrderCreate,
    db: Session = Depends(get_db),
    admin: str = Depends(require_admin),
):
    """Create a new service order"""
    if service.status.lower() not in {"draft", "waiting", "scheduled"}:
        raise HTTPException(status_code=422, detail="Service baru hanya boleh berstatus draft, waiting, atau scheduled")
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
async def update_service(
    service_id: int,
    service: schemas.ServiceOrderCreate,
    db: Session = Depends(get_db),
    admin: str = Depends(require_admin),
):
    """Update service"""
    db_service = db.query(models.ServiceOrder).filter(models.ServiceOrder.id == service_id).first()
    if not db_service:
        raise HTTPException(status_code=404, detail="Service tidak ditemukan")

    next_status = service.status.lower()
    if next_status != db_service.status.lower() and next_status not in STATUS_TRANSITIONS.get(db_service.status.lower(), set()):
        raise HTTPException(status_code=409, detail=f"Status tidak dapat berubah dari {db_service.status} menjadi {service.status}")

    db_service.vehicle_id = service.vehicle_id
    db_service.mechanic_id = service.mechanic_id
    db_service.complaint = service.complaint
    db_service.diagnosis = service.diagnosis
    db_service.status = next_status
    if next_status == "completed" and db_service.completed_at is None:
        db_service.completed_at = datetime.utcnow()
    db_service.total_cost = service.total_cost

    db.commit()
    db.refresh(db_service)
    return db_service


@router.patch("/{service_id}/status", response_model=schemas.ServiceOrderResponse)
async def update_service_status(
    service_id: int,
    status_update: schemas.ServiceStatusUpdate,
    db: Session = Depends(get_db),
    admin: str = Depends(require_admin),
):
    """Advance a service order through the workshop workflow."""
    db_service = db.query(models.ServiceOrder).filter(models.ServiceOrder.id == service_id).first()
    if not db_service:
        raise HTTPException(status_code=404, detail="Service tidak ditemukan")

    current_status = db_service.status.lower()
    next_status = status_update.status.lower()
    allowed_statuses = set(STATUS_TRANSITIONS)
    if next_status not in allowed_statuses:
        raise HTTPException(status_code=422, detail="Status servis tidak valid")
    if next_status not in STATUS_TRANSITIONS.get(current_status, set()):
        raise HTTPException(
            status_code=409,
            detail=f"Status tidak dapat berubah dari {db_service.status} menjadi {status_update.status}",
        )

    db_service.status = next_status
    if next_status == "completed":
        db_service.completed_at = datetime.utcnow()
    db.commit()
    db.refresh(db_service)
    return db_service


@router.delete("/{service_id}")
async def delete_service(
    service_id: int,
    db: Session = Depends(get_db),
    admin: str = Depends(require_admin),
):
    """Delete service"""
    db_service = db.query(models.ServiceOrder).filter(models.ServiceOrder.id == service_id).first()
    if not db_service:
        raise HTTPException(status_code=404, detail="Service tidak ditemukan")

    db.delete(db_service)
    db.commit()
    return {"status": "deleted"}


@router.post("/{service_id}/items", response_model=schemas.ServiceItemResponse, status_code=201)
async def add_service_item(
    service_id: int,
    item: schemas.ServiceItemCreate,
    db: Session = Depends(get_db),
    admin: str = Depends(require_admin),
):
    service = db.query(models.ServiceOrder).filter(models.ServiceOrder.id == service_id).with_for_update().first()
    sparepart = db.query(models.Sparepart).filter(models.Sparepart.id == item.sparepart_id).with_for_update().first()
    if not service:
        raise HTTPException(status_code=404, detail="Service tidak ditemukan")
    if not sparepart:
        raise HTTPException(status_code=404, detail="Sparepart tidak ditemukan")
    if item.quantity <= 0:
        raise HTTPException(status_code=422, detail="Quantity harus lebih besar dari nol")
    if sparepart.stock < item.quantity:
        raise HTTPException(status_code=409, detail="Stok sparepart tidak mencukupi")

    service_item = models.ServiceItem(
        service_order_id=service_id,
        sparepart_id=item.sparepart_id,
        quantity=item.quantity,
        price=sparepart.price,
    )
    sparepart.stock -= item.quantity
    service.total_cost = (service.total_cost or 0) + (sparepart.price * item.quantity)
    db.add(service_item)
    db.commit()
    db.refresh(service_item)
    return service_item


@router.delete("/{service_id}/items/{item_id}")
async def remove_service_item(
    service_id: int,
    item_id: int,
    db: Session = Depends(get_db),
    admin: str = Depends(require_admin),
):
    item = (
        db.query(models.ServiceItem)
        .filter(models.ServiceItem.id == item_id, models.ServiceItem.service_order_id == service_id)
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="Service item tidak ditemukan")
    sparepart = db.query(models.Sparepart).filter(models.Sparepart.id == item.sparepart_id).with_for_update().first()
    service = db.query(models.ServiceOrder).filter(models.ServiceOrder.id == service_id).with_for_update().first()
    sparepart.stock += item.quantity
    service.total_cost = max(0, (service.total_cost or 0) - (item.price * item.quantity))
    db.delete(item)
    db.commit()
    return {"status": "deleted", "restored_stock": item.quantity}


@router.get("/{service_id}/invoice", response_model=schemas.InvoiceResponse)
async def get_invoice(service_id: int, db: Session = Depends(get_db)):
    service = db.query(models.ServiceOrder).filter(models.ServiceOrder.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service tidak ditemukan")
    items = [
        {
            "id": item.id,
            "sparepart_id": item.sparepart_id,
            "name": item.sparepart.name,
            "quantity": item.quantity,
            "unit_price": float(item.price),
            "subtotal": float(item.price * item.quantity),
        }
        for item in service.service_items
    ]
    subtotal = sum(item["subtotal"] for item in items)
    return {"service_id": service.id, "status": service.status, "subtotal": subtotal, "total": float(service.total_cost), "items": items}
