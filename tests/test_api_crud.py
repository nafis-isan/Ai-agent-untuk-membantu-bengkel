import os
from uuid import uuid4

os.environ.setdefault("GEMINI_API_KEY", "test-key")
os.environ.setdefault("ADMIN_USERNAME", "admin")
os.environ.setdefault("ADMIN_PASSWORD", "test-password")
os.environ.setdefault("ADMIN_TOKEN_SECRET", "test-secret")

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.connection import Base
from app.database.dependencies import get_db
from app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_bengkel.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)
AUTH_HEADERS = {
    "Authorization": f"Bearer {client.post('/auth/login', json={'username': 'admin', 'password': 'test-password'}).json()['access_token']}"
}


def test_customers_crud_flow():
    create_response = client.post(
        "/customers/",
        json={
            "name": "Budi",
            "phone": "08123456789",
            "email": "budi@example.com",
            "address": "Bandung",
        },
        headers=AUTH_HEADERS,
    )
    assert create_response.status_code == 201

    customer_id = create_response.json()["id"]

    list_response = client.get("/customers/")
    assert list_response.status_code == 200
    assert any(item["id"] == customer_id for item in list_response.json())

    update_response = client.put(
        f"/customers/{customer_id}",
        json={
            "name": "Budi Updated",
            "phone": "08123456789",
            "email": "budi.updated@example.com",
            "address": "Jakarta",
        },
        headers=AUTH_HEADERS,
    )
    assert update_response.status_code == 200
    assert update_response.json()["name"] == "Budi Updated"

    delete_response = client.delete(f"/customers/{customer_id}", headers=AUTH_HEADERS)
    assert delete_response.status_code == 200
    assert delete_response.json()["status"] == "deleted"


def test_vehicles_and_spareparts_can_be_created():
    customer_response = client.post(
        "/customers/",
        json={
            "name": "Ani",
            "phone": "08234567890",
            "email": "ani@example.com",
            "address": "Yogyakarta",
        },
        headers=AUTH_HEADERS,
    )
    customer_id = customer_response.json()["id"]

    vehicle_response = client.post(
        "/vehicles/",
        json={
            "customer_id": customer_id,
            "plate_number": "B 1234 XYZ",
            "brand": "Toyota",
            "model": "Avanza",
            "year": 2022,
            "vehicle_type": "Mobil Penumpang",
        },
        headers=AUTH_HEADERS,
    )
    assert vehicle_response.status_code == 201

    sparepart_response = client.post(
        "/spareparts/",
        json={
            "part_number": "OIL-001",
            "name": "Filter Oli",
            "brand": "Bosch",
            "price": 35000,
            "stock": 10,
            "minimum_stock": 5,
        },
        headers=AUTH_HEADERS,
    )
    assert sparepart_response.status_code == 201


def test_service_items_status_invoice_and_health():
    suffix = uuid4().hex[:8]
    customer = client.post("/customers/", json={"name": "Service Test", "phone": suffix}, headers=AUTH_HEADERS).json()
    vehicle = client.post("/vehicles/", json={"customer_id": customer["id"], "plate_number": f"T {suffix}", "brand": "Honda", "model": "Brio", "year": 2023, "vehicle_type": "Mobil"}, headers=AUTH_HEADERS).json()
    part = client.post("/spareparts/", json={"part_number": f"P-{suffix}", "name": "Oli", "price": 10000, "stock": 2, "minimum_stock": 1}, headers=AUTH_HEADERS).json()
    service = client.post("/services/", json={"vehicle_id": vehicle["id"], "complaint": "Ganti oli", "status": "draft"}, headers=AUTH_HEADERS).json()

    item = client.post(f"/services/{service['id']}/items", json={"sparepart_id": part["id"], "quantity": 1}, headers=AUTH_HEADERS)
    assert item.status_code == 201
    assert client.get(f"/spareparts/{part['id']}").json()["stock"] == 1
    invoice = client.get(f"/services/{service['id']}/invoice")
    assert invoice.status_code == 200
    assert invoice.json()["total"] == 10000

    illegal = client.patch(f"/services/{service['id']}/status", json={"status": "completed"}, headers=AUTH_HEADERS)
    assert illegal.status_code == 409
    for status in ("waiting", "in_progress", "completed"):
        response = client.patch(f"/services/{service['id']}/status", json={"status": status}, headers=AUTH_HEADERS)
        assert response.status_code == 200
    assert client.get("/health").json()["status"] == "ok"
