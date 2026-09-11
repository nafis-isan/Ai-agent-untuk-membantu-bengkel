import os

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func

from app.api.auth import router as auth_router
from app.api.customers import router as customer_router
from app.api.vehicles import router as vehicle_router
from app.api.spareparts import router as sparepart_router
from app.api.services import router as service_router
from app.api.chat import router as chat_router
from app.api.insights import router as insights_router
from app.api.appointments import router as appointment_router
from app.api.whatsapp import router as whatsapp_router
from app.database.init_db import init_database
from app.database.models import AgentUsage
from app.database.dependencies import get_db
from app.auth import require_admin


app = FastAPI(
    title="BengkelAI",
    description="AI Agent untuk membantu operasional bengkel",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        origin.strip()
        for origin in os.getenv("FRONTEND_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000").split(",")
        if origin.strip()
    ],
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
app.include_router(insights_router)
app.include_router(appointment_router)
app.include_router(whatsapp_router)
app.include_router(auth_router)


@app.get("/")
def root():
    return {
        "message": "BengkelAI API is running"
    }


@app.get("/health")
def health():
    from sqlalchemy import text
    from app.database.connection import engine

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"status": "ok", "database": "ok"}
    except Exception:
        return {"status": "degraded", "database": "unavailable"}


@app.get("/metrics")
def metrics(db=Depends(get_db), admin: str = Depends(require_admin)):
    total_requests, total_cost = db.query(
        func.count(AgentUsage.id), func.coalesce(func.sum(AgentUsage.estimated_cost), 0)
    ).one()
    return {"agent_requests": total_requests, "estimated_cost_usd": float(total_cost or 0)}