from datetime import datetime

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.database.models import Customer, ServiceOrder, Sparepart, Vehicle


def _vehicle_data(vehicle: Vehicle) -> dict:
    return {
        "id": vehicle.id,
        "plate_number": vehicle.plate_number,
        "brand": vehicle.brand,
        "model": vehicle.model,
        "year": vehicle.year,
        "vehicle_type": vehicle.vehicle_type,
        "customer_id": vehicle.customer_id,
    }


def search_vehicle(plate_number: str, db: Session) -> dict:
    vehicle = db.query(Vehicle).filter(Vehicle.plate_number.ilike(f"%{plate_number}%")).first()
    if not vehicle:
        return {"found": False, "message": "Kendaraan tidak ditemukan."}
    return {"found": True, "vehicle": _vehicle_data(vehicle)}


def search_customer(query: str, db: Session) -> dict:
    customers = (
        db.query(Customer)
        .filter(or_(Customer.name.ilike(f"%{query}%"), Customer.phone.ilike(f"%{query}%")))
        .limit(10)
        .all()
    )
    return {
        "customers": [
            {"id": item.id, "name": item.name, "phone": item.phone, "email": item.email, "address": item.address}
            for item in customers
        ]
    }


def check_spareparts(low_stock_only: bool, db: Session) -> dict:
    query = db.query(Sparepart)
    if low_stock_only:
        query = query.filter(Sparepart.stock <= Sparepart.minimum_stock)
    parts = query.order_by(Sparepart.stock.asc()).limit(20).all()
    return {
        "spareparts": [
            {"id": item.id, "part_number": item.part_number, "name": item.name, "brand": item.brand, "stock": item.stock, "minimum_stock": item.minimum_stock, "price": float(item.price)}
            for item in parts
        ]
    }


def get_service_history(vehicle_id: int | None, db: Session) -> dict:
    query = db.query(ServiceOrder).order_by(ServiceOrder.created_at.desc())
    if vehicle_id is not None:
        query = query.filter(ServiceOrder.vehicle_id == vehicle_id)
    services = query.limit(20).all()
    return {
        "services": [
            {"id": item.id, "vehicle_id": item.vehicle_id, "complaint": item.complaint, "diagnosis": item.diagnosis, "status": item.status, "total_cost": float(item.total_cost), "created_at": item.created_at.isoformat()}
            for item in services
        ]
    }


def prepare_service_creation(vehicle_id: int, complaint: str, diagnosis: str | None, status: str, total_cost: float, db: Session) -> dict:
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        return {"confirmation_required": False, "error": "Kendaraan tidak ditemukan."}
    return {
        "confirmation_required": True,
        "message": "Order servis siap dibuat setelah konfirmasi pengguna.",
        "action": {
            "type": "create_service",
            "label": "Konfirmasi buat servis",
            "payload": {"vehicle_id": vehicle_id, "mechanic_id": None, "complaint": complaint, "diagnosis": diagnosis, "status": status, "total_cost": total_cost},
        },
        "vehicle": _vehicle_data(vehicle),
    }


def create_service(payload: dict, db: Session) -> dict:
    vehicle = db.query(Vehicle).filter(Vehicle.id == payload["vehicle_id"]).first()
    if not vehicle:
        raise ValueError("Kendaraan tidak ditemukan.")
    service = ServiceOrder(**payload)
    db.add(service)
    db.commit()
    db.refresh(service)
    return {"id": service.id, "vehicle_id": service.vehicle_id, "status": service.status, "complaint": service.complaint, "total_cost": float(service.total_cost)}


def prepare_service_status_update(service_id: int, status: str, db: Session) -> dict:
    service = db.query(ServiceOrder).filter(ServiceOrder.id == service_id).first()
    if not service:
        return {"confirmation_required": False, "error": "Service tidak ditemukan."}
    return {
        "confirmation_required": True,
        "message": f"Status servis #{service_id} siap diubah dari {service.status} menjadi {status} setelah konfirmasi pengguna.",
        "action": {
            "type": "update_service_status",
            "label": f"Ubah status servis #{service_id} menjadi {status}",
            "payload": {"service_id": service_id, "status": status},
        },
        "service": {"id": service.id, "status": service.status, "vehicle_id": service.vehicle_id},
    }


def update_service_status(payload: dict, db: Session) -> dict:
    service = db.query(ServiceOrder).filter(ServiceOrder.id == payload["service_id"]).first()
    if not service:
        raise ValueError("Service tidak ditemukan.")

    transitions = {
        "draft": {"waiting"},
        "waiting": {"in_progress"},
        "in_progress": {"completed"},
    }
    current_status = service.status.lower()
    next_status = payload["status"].lower()
    if next_status not in transitions.get(current_status, set()):
        raise ValueError(f"Status tidak dapat berubah dari {service.status} menjadi {next_status}.")

    service.status = next_status
    if next_status == "completed":
        service.completed_at = datetime.utcnow()
    db.commit()
    db.refresh(service)
    return {"id": service.id, "vehicle_id": service.vehicle_id, "status": service.status}


TOOL_DECLARATIONS = [
    {"name": "search_vehicle", "description": "Mencari kendaraan berdasarkan nomor plat.", "parameters": {"type": "OBJECT", "properties": {"plate_number": {"type": "STRING"}}, "required": ["plate_number"]}},
    {"name": "search_customer", "description": "Mencari pelanggan berdasarkan nama atau nomor telepon.", "parameters": {"type": "OBJECT", "properties": {"query": {"type": "STRING"}}, "required": ["query"]}},
    {"name": "check_spareparts", "description": "Mengecek stok suku cadang. Gunakan low_stock_only true untuk stok rendah.", "parameters": {"type": "OBJECT", "properties": {"low_stock_only": {"type": "BOOLEAN"}}, "required": ["low_stock_only"]}},
    {"name": "get_service_history", "description": "Membaca riwayat servis, opsional berdasarkan vehicle_id.", "parameters": {"type": "OBJECT", "properties": {"vehicle_id": {"type": "INTEGER"}}}},
    {"name": "prepare_service_creation", "description": "Menyiapkan order servis untuk konfirmasi pengguna. Tidak menyimpan data.", "parameters": {"type": "OBJECT", "properties": {"vehicle_id": {"type": "INTEGER"}, "complaint": {"type": "STRING"}, "diagnosis": {"type": "STRING"}, "status": {"type": "STRING"}, "total_cost": {"type": "NUMBER"}}, "required": ["vehicle_id", "complaint", "status", "total_cost"]}},
    {"name": "prepare_service_status_update", "description": "Menyiapkan perubahan status servis untuk konfirmasi pengguna. Gunakan status draft, waiting, in_progress, atau completed.", "parameters": {"type": "OBJECT", "properties": {"service_id": {"type": "INTEGER"}, "status": {"type": "STRING"}}, "required": ["service_id", "status"]}},
]

TOOL_FUNCTIONS = {
    "search_vehicle": search_vehicle,
    "search_customer": search_customer,
    "check_spareparts": check_spareparts,
    "get_service_history": get_service_history,
    "prepare_service_creation": prepare_service_creation,
    "prepare_service_status_update": prepare_service_status_update,
}
