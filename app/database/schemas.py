from pydantic import BaseModel, ConfigDict, Field
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
    customer_id: int = Field(gt=0)


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


class ServiceItemCreate(BaseModel):
    sparepart_id: int = Field(gt=0)
    quantity: int = Field(gt=0)


class ServiceItemResponse(ServiceItemCreate):
    id: int
    service_order_id: int
    price: float

    model_config = ConfigDict(from_attributes=True)


# =========================
# SERVICE ORDER
# =========================

class ServiceOrderBase(BaseModel):
    vehicle_id: int = Field(gt=0)
    mechanic_id: int | None = None
    complaint: str
    diagnosis: str | None = None
    status: str = "waiting"
    total_cost: float = 0.0


class ServiceOrderCreate(ServiceOrderBase):
    pass


class ServiceStatusUpdate(BaseModel):
    status: str


class ServiceOrderResponse(ServiceOrderBase):
    id: int
    created_at: datetime
    completed_at: datetime | None = None
    service_items: list[ServiceItemResponse] = []

    model_config = ConfigDict(from_attributes=True)


class AppointmentCreate(BaseModel):
    customer_id: int = Field(gt=0)
    vehicle_id: int = Field(gt=0)
    scheduled_at: datetime
    complaint: str = Field(min_length=2, max_length=2000)
    status: str = Field(default="scheduled", pattern="^(scheduled|confirmed|cancelled|completed)$")


class AppointmentResponse(AppointmentCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class InvoiceResponse(BaseModel):
    service_id: int
    status: str
    subtotal: float
    total: float
    items: list[dict]