from .connection import SessionLocal
from .models import Customer, Vehicle, Mechanic, Sparepart


def seed_database():
    db = SessionLocal()

    try:
        customer1 = Customer(
            name="Budi Santoso",
            phone="081234567890",
            email="budi@example.com",
            address="Garut"
        )

        customer2 = Customer(
            name="Andi Setiawan",
            phone="082345678901",
            email="andi@example.com",
            address="Bandung"
        )

        db.add_all([customer1, customer2])
        db.flush()

        vehicle1 = Vehicle(
            customer_id=customer1.id,
            plate_number="D 1234 ABC",
            brand="Toyota",
            model="Avanza",
            year=2018,
            vehicle_type="Mobil"
        )

        vehicle2 = Vehicle(
            customer_id=customer2.id,
            plate_number="Z 5678 XYZ",
            brand="Honda",
            model="Vario 160",
            year=2023,
            vehicle_type="Motor"
        )

        db.add_all([vehicle1, vehicle2])

        mechanic1 = Mechanic(
            name="Rudi",
            specialization="Mesin",
            phone="083456789012"
        )

        mechanic2 = Mechanic(
            name="Deni",
            specialization="Kelistrikan",
            phone="084567890123"
        )

        db.add_all([mechanic1, mechanic2])

        sparepart1 = Sparepart(
            part_number="OLI-001",
            name="Oli Mesin 10W-40",
            brand="Federal",
            price=55000,
            stock=20,
            minimum_stock=5
        )

        sparepart2 = Sparepart(
            part_number="BUSI-001",
            name="Busi Vario 160",
            brand="NGK",
            price=35000,
            stock=10,
            minimum_stock=3
        )

        sparepart3 = Sparepart(
            part_number="AKI-001",
            name="Aki Motor",
            brand="GS Astra",
            price=280000,
            stock=2,
            minimum_stock=3
        )

        db.add_all([
            sparepart1,
            sparepart2,
            sparepart3
        ])

        db.commit()

        print("Sample data inserted successfully!")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()