"""Customers API Endpoints"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database import models, schemas

router = APIRouter(prefix="/api/customers", tags=["customers"])


@router.get("/")
async def get_customers(db: Session = Depends(get_db)):
    """Get all customers"""
    return db.query(models.Customer).all()


@router.get("/{customer_id}")
async def get_customer(customer_id: int, db: Session = Depends(get_db)):
    """Get customer by ID"""
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()


@router.post("/")
async def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    """Create a new customer"""
    db_customer = models.Customer(**customer.model_dump())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


@router.put("/{customer_id}")
async def update_customer(customer_id: int, customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    """Update customer"""
    db_customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if db_customer:
        for key, value in customer.model_dump().items():
            setattr(db_customer, key, value)
        db.commit()
        db.refresh(db_customer)
    return db_customer


@router.delete("/{customer_id}")
async def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    """Delete customer"""
    db_customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if db_customer:
        db.delete(db_customer)
        db.commit()
    return {"status": "deleted"}
