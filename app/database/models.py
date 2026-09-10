from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .connection import Base


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    phone: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    email: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    address: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    vehicles: Mapped[list["Vehicle"]] = relationship(
        back_populates="customer"
    )


class Vehicle(Base):
    __tablename__ = "vehicles"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id"),
        nullable=False
    )

    plate_number: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False
    )

    brand: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    model: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    year: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    vehicle_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    customer: Mapped["Customer"] = relationship(
        back_populates="vehicles"
    )

    service_orders: Mapped[list["ServiceOrder"]] = relationship(
        back_populates="vehicle"
    )


class Mechanic(Base):
    __tablename__ = "mechanics"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    specialization: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    phone: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
    )

    service_orders: Mapped[list["ServiceOrder"]] = relationship(
        back_populates="mechanic"
    )


class Sparepart(Base):
    __tablename__ = "spareparts"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    part_number: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    brand: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    price: Mapped[float] = mapped_column(
        Numeric(12, 2),
        nullable=False
    )

    stock: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )

    minimum_stock: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )

    service_items: Mapped[list["ServiceItem"]] = relationship(
        back_populates="sparepart"
    )


class ServiceOrder(Base):
    __tablename__ = "service_orders"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    vehicle_id: Mapped[int] = mapped_column(
        ForeignKey("vehicles.id"),
        nullable=False
    )

    mechanic_id: Mapped[int | None] = mapped_column(
        ForeignKey("mechanics.id"),
        nullable=True
    )

    complaint: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    diagnosis: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="waiting",
        nullable=False
    )

    total_cost: Mapped[float] = mapped_column(
        Numeric(12, 2),
        default=0,
        nullable=False
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    vehicle: Mapped["Vehicle"] = relationship(
        back_populates="service_orders"
    )

    mechanic: Mapped["Mechanic | None"] = relationship(
        back_populates="service_orders"
    )

    service_items: Mapped[list["ServiceItem"]] = relationship(
        back_populates="service_order"
    )


class ServiceItem(Base):
    __tablename__ = "service_items"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    service_order_id: Mapped[int] = mapped_column(
        ForeignKey("service_orders.id"),
        nullable=False
    )

    sparepart_id: Mapped[int] = mapped_column(
        ForeignKey("spareparts.id"),
        nullable=False
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    price: Mapped[float] = mapped_column(
        Numeric(12, 2),
        nullable=False
    )

    service_order: Mapped["ServiceOrder"] = relationship(
        back_populates="service_items"
    )

    sparepart: Mapped["Sparepart"] = relationship(
        back_populates="service_items"
    )


class AgentMessage(Base):
    __tablename__ = "agent_messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    session_id: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)