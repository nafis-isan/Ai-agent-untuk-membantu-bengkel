from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.database.models import Sparepart
from app.database.schemas import SparepartCreate, SparepartResponse


router = APIRouter(
    prefix="/spareparts",
    tags=["Spareparts"]
)


@router.get(
    "/",
    response_model=list[SparepartResponse]
)
def get_spareparts(
    db: Session = Depends(get_db)
):
    return db.query(Sparepart).all()


@router.get(
    "/{sparepart_id}",
    response_model=SparepartResponse
)
def get_sparepart(
    sparepart_id: int,
    db: Session = Depends(get_db)
):
    sparepart = (
        db.query(Sparepart)
        .filter(Sparepart.id == sparepart_id)
        .first()
    )

    if not sparepart:
        raise HTTPException(
            status_code=404,
            detail="Sparepart tidak ditemukan"
        )

    return sparepart


@router.post(
    "/",
    response_model=SparepartResponse,
    status_code=201
)
def create_sparepart(
    sparepart_data: SparepartCreate,
    db: Session = Depends(get_db)
):
    sparepart = Sparepart(
        part_number=sparepart_data.part_number,
        name=sparepart_data.name,
        brand=sparepart_data.brand,
        price=sparepart_data.price,
        stock=sparepart_data.stock,
        minimum_stock=sparepart_data.minimum_stock,
    )

    db.add(sparepart)
    db.commit()
    db.refresh(sparepart)

    return sparepart


@router.put(
    "/{sparepart_id}",
    response_model=SparepartResponse
)
def update_sparepart(
    sparepart_id: int,
    sparepart_data: SparepartCreate,
    db: Session = Depends(get_db)
):
    sparepart = db.query(Sparepart).filter(Sparepart.id == sparepart_id).first()
    if not sparepart:
        raise HTTPException(
            status_code=404,
            detail="Sparepart tidak ditemukan"
        )

    sparepart.part_number = sparepart_data.part_number
    sparepart.name = sparepart_data.name
    sparepart.brand = sparepart_data.brand
    sparepart.price = sparepart_data.price
    sparepart.stock = sparepart_data.stock
    sparepart.minimum_stock = sparepart_data.minimum_stock

    db.commit()
    db.refresh(sparepart)

    return sparepart


@router.delete(
    "/{sparepart_id}"
)
def delete_sparepart(
    sparepart_id: int,
    db: Session = Depends(get_db)
):
    sparepart = db.query(Sparepart).filter(Sparepart.id == sparepart_id).first()
    if not sparepart:
        raise HTTPException(
            status_code=404,
            detail="Sparepart tidak ditemukan"
        )

    db.delete(sparepart)
    db.commit()

    return {"status": "deleted"}