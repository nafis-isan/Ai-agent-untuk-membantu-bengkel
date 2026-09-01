from pydantic import BaseModel, ConfigDict
from datetime import datetime


# =========================
# CUSTOMER
# =========================

class CustomerBase(BaseModel):
    name: str
    phone: str
    email: str | None = None
    address: str | None = None


class CustomerCreate(CustomerBase):
    pass


class CustomerResponse(CustomerBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# =========================
# VEHICLE
# =========================

class VehicleBase(BaseModel):
    plate_number: str
    brand: str
    model: str
    year: int
    vehicle_type: str


class VehicleCreate(VehicleBase):
    customer_id: int


class VehicleResponse(VehicleBase):
    id: int
    customer_id: int

    model_config = ConfigDict(from_attributes=True)


# =========================
# SPAREPART
# =========================

class SparepartBase(BaseModel):
    part_number: str
    name: str
    brand: str | None = None
    price: float
    stock: int
    minimum_stock: int


class SparepartCreate(SparepartBase):
    pass


class SparepartResponse(SparepartBase):
    id: int

    model_config = ConfigDict(from_attributes=True)