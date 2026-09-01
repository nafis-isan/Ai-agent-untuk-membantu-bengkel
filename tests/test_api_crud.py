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


def test_customers_crud_flow():
    create_response = client.post(
        "/customers/",
        json={
            "name": "Budi",
            "phone": "08123456789",
            "email": "budi@example.com",
            "address": "Bandung",
        },
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
    )
    assert update_response.status_code == 200
    assert update_response.json()["name"] == "Budi Updated"

    delete_response = client.delete(f"/customers/{customer_id}")
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
    )
    assert sparepart_response.status_code == 201
