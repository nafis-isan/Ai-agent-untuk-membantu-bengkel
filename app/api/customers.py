from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.database.models import Customer
from app.database.schemas import (
    CustomerCreate,
    CustomerResponse,
)
from app.auth import require_admin


router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)


@router.get(
    "/",
    response_model=list[CustomerResponse]
)
def get_customers(
    db: Session = Depends(get_db)
):
    return db.query(Customer).all()


@router.get(
    "/{customer_id}",
    response_model=CustomerResponse
)
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):
    customer = (
        db.query(Customer)
        .filter(Customer.id == customer_id)
        .first()
    )

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer tidak ditemukan"
        )

    return customer


@router.post(
    "/",
    response_model=CustomerResponse,
    status_code=201
)
def create_customer(
    customer_data: CustomerCreate,
    db: Session = Depends(get_db),
    admin: str = Depends(require_admin),
):
    customer = Customer(
        name=customer_data.name,
        phone=customer_data.phone,
        email=customer_data.email,
        address=customer_data.address
    )

    db.add(customer)
    db.commit()
    db.refresh(customer)

    return customer


@router.put(
    "/{customer_id}",
    response_model=CustomerResponse
)
def update_customer(
    customer_id: int,
    customer_data: CustomerCreate,
    db: Session = Depends(get_db),
    admin: str = Depends(require_admin),
):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer tidak ditemukan"
        )

    customer.name = customer_data.name
    customer.phone = customer_data.phone
    customer.email = customer_data.email
    customer.address = customer_data.address

    db.commit()
    db.refresh(customer)

    return customer


@router.delete(
    "/{customer_id}"
)
def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    admin: str = Depends(require_admin),
):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer tidak ditemukan"
        )

    db.delete(customer)
    db.commit()

    return {"status": "deleted"}