from fastapi import FastAPI

from app.api.customers import router as customer_router
from app.api.vehicles import router as vehicle_router
from app.api.spareparts import router as sparepart_router


app = FastAPI(
    title="BengkelAI",
    description="AI Agent untuk membantu operasional bengkel",
    version="1.0.0"
)


app.include_router(customer_router)
app.include_router(vehicle_router)


@app.get("/")
def root():
    return {
        "message": "BengkelAI API is running"
    }