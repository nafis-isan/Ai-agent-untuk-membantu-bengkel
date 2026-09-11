from datetime import datetime, timedelta
from uuid import uuid4

from tests.test_api_crud import AUTH_HEADERS, client


def test_appointment_create_and_status_update():
    suffix = uuid4().hex[:8]
    customer = client.post(
        "/customers/",
        json={"name": "Appointment Test", "phone": suffix},
        headers=AUTH_HEADERS,
    ).json()
    vehicle = client.post(
        "/vehicles/",
        json={
            "customer_id": customer["id"],
            "plate_number": f"A {suffix}",
            "brand": "Toyota",
            "model": "Yaris",
            "year": 2024,
            "vehicle_type": "Mobil",
        },
        headers=AUTH_HEADERS,
    ).json()
    appointment = client.post(
        "/appointments/",
        json={
            "customer_id": customer["id"],
            "vehicle_id": vehicle["id"],
            "scheduled_at": (datetime.utcnow() + timedelta(days=1)).isoformat(),
            "complaint": "Pemeriksaan rem",
        },
        headers=AUTH_HEADERS,
    )
    assert appointment.status_code == 201
    appointment_id = appointment.json()["id"]

    updated = client.patch(
        f"/appointments/{appointment_id}/status",
        json={"status": "confirmed"},
        headers=AUTH_HEADERS,
    )
    assert updated.status_code == 200
    assert updated.json()["status"] == "confirmed"
