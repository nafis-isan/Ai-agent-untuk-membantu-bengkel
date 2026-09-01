"""Database Schemas (Pydantic Models)"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CustomerBase(BaseModel):
    """Customer Base Schema"""
    name: str
    phone: str
    email: str
    address: str


class CustomerCreate(CustomerBase):
    """Customer Create Schema"""
    pass


class Customer(CustomerBase):
    """Customer Schema"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class VehicleBase(BaseModel):
    """Vehicle Base Schema"""
    customer_id: int
    brand: str
    model: str
    year: int
    license_plate: str


class VehicleCreate(VehicleBase):
    """Vehicle Create Schema"""
    pass


class Vehicle(VehicleBase):
    """Vehicle Schema"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ServiceBase(BaseModel):
    """Service Base Schema"""
    vehicle_id: int
    service_date: datetime
    description: str
    cost: int


class ServiceCreate(ServiceBase):
    """Service Create Schema"""
    pass


class Service(ServiceBase):
    """Service Schema"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
