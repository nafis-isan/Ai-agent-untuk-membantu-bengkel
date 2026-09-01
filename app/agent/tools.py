from sqlalchemy.orm import Session

from app.database.models import Vehicle


def search_vehicle(
    plate_number: str,
    db: Session
) -> dict:

    vehicle = (
        db.query(Vehicle)
        .filter(
            Vehicle.plate_number == plate_number
        )
        .first()
    )

    if not vehicle:
        return {
            "found": False,
            "message": "Kendaraan tidak ditemukan."
        }

    return {
        "found": True,
        "vehicle": {
            "id": vehicle.id,
            "plate_number": vehicle.plate_number,
            "brand": vehicle.brand,
            "model": vehicle.model,
            "year": vehicle.year,
            "vehicle_type": vehicle.vehicle_type,
            "customer_id": vehicle.customer_id
        }
    }

SEARCH_VEHICLE_TOOL = {
    "type": "function",
    "name": "search_vehicle",
    "description": (
        "Mencari data kendaraan berdasarkan nomor plat "
        "kendaraan di database bengkel."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "plate_number": {
                "type": "string",
                "description": (
                    "Nomor plat kendaraan, "
                    "contoh: D 1234 ABC"
                )
            }
        },
        "required": ["plate_number"]
    }
}