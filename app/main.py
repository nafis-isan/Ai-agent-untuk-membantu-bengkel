from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.customers import router as customer_router
from app.api.vehicles import router as vehicle_router
from app.api.spareparts import router as sparepart_router
from app.api.services import router as service_router
from app.api.chat import router as chat_router
from app.database.init_db import init_database


app = FastAPI(
    title="BengkelAI",
    description="AI Agent untuk membantu operasional bengkel",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


init_database()


app.include_router(customer_router)
app.include_router(vehicle_router)
app.include_router(sparepart_router)
app.include_router(service_router)
app.include_router(chat_router)


@app.get("/")
def root():
    return {
        "message": "BengkelAI API is running"
    }