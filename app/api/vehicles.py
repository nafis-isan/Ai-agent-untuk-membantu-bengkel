from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.database.models import Vehicle, Customer
from app.database.schemas import (
    VehicleCreate,
    VehicleResponse,
)
from app.auth import require_admin


router = APIRouter(
    prefix="/vehicles",
    tags=["Vehicles"]
)


@router.get(
    "/",
    response_model=list[VehicleResponse]
)
def get_vehicles(
    db: Session = Depends(get_db)
):
    return db.query(Vehicle).all()


@router.get(
    "/{vehicle_id}",
    response_model=VehicleResponse
)
def get_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db)
):
    vehicle = (
        db.query(Vehicle)
        .filter(Vehicle.id == vehicle_id)
        .first()
    )

    if not vehicle:
        raise HTTPException(
            status_code=404,
            detail="Kendaraan tidak ditemukan"
        )

    return vehicle


@router.post(
    "/",
    response_model=VehicleResponse,
    status_code=201
)
def create_vehicle(
    vehicle_data: VehicleCreate,
    db: Session = Depends(get_db),
    admin: str = Depends(require_admin),
):
    customer = (
        db.query(Customer)
        .filter(Customer.id == vehicle_data.customer_id)
        .first()
    )

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer tidak ditemukan"
        )

    vehicle = Vehicle(
        customer_id=vehicle_data.customer_id,
        plate_number=vehicle_data.plate_number,
        brand=vehicle_data.brand,
        model=vehicle_data.model,
        year=vehicle_data.year,
        vehicle_type=vehicle_data.vehicle_type
    )

    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)

    return vehicle


@router.put(
    "/{vehicle_id}",
    response_model=VehicleResponse
)
def update_vehicle(
    vehicle_id: int,
    vehicle_data: VehicleCreate,
    db: Session = Depends(get_db),
    admin: str = Depends(require_admin),
):
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(
            status_code=404,
            detail="Kendaraan tidak ditemukan"
        )

    customer = db.query(Customer).filter(Customer.id == vehicle_data.customer_id).first()
    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer tidak ditemukan"
        )

    vehicle.customer_id = vehicle_data.customer_id
    vehicle.plate_number = vehicle_data.plate_number
    vehicle.brand = vehicle_data.brand
    vehicle.model = vehicle_data.model
    vehicle.year = vehicle_data.year
    vehicle.vehicle_type = vehicle_data.vehicle_type

    db.commit()
    db.refresh(vehicle)

    return vehicle


@router.delete(
    "/{vehicle_id}"
)
def delete_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db),
    admin: str = Depends(require_admin),
):
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        raise HTTPException(
            status_code=404,
            detail="Kendaraan tidak ditemukan"
        )

    db.delete(vehicle)
    db.commit()

    return {"status": "deleted"}