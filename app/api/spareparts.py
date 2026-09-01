from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.database.models import Sparepart
from app.database.schemas import SparepartResponse


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
    "/{part_number}",
    response_model=SparepartResponse
)
def get_sparepart(
    part_number: str,
    db: Session = Depends(get_db)
):
    sparepart = (
        db.query(Sparepart)
        .filter(
            Sparepart.part_number == part_number
        )
        .first()
    )

    if not sparepart:
        raise HTTPException(
            status_code=404,
            detail="Sparepart tidak ditemukan"
        )

    return sparepart