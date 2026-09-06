from datetime import datetime, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.database.models import ServiceOrder, Sparepart


router = APIRouter(prefix="/insights", tags=["Insights"])


@router.get("/")
def get_insights(db: Session = Depends(get_db)):
    active_services = db.query(ServiceOrder).filter(ServiceOrder.status.in_(["waiting", "in_progress", "scheduled"])).count()
    low_stock = db.query(Sparepart).filter(Sparepart.stock <= Sparepart.minimum_stock).count()
    old_waiting = db.query(ServiceOrder).filter(ServiceOrder.status == "waiting", ServiceOrder.created_at <= datetime.utcnow() - timedelta(days=2)).count()
    insights = []
    if active_services:
        insights.append({"type": "active_services", "tone": "blue", "title": f"{active_services} servis sedang aktif", "description": "Pantau antrean agar pekerjaan tidak tertunda."})
    if low_stock:
        insights.append({"type": "low_stock", "tone": "amber", "title": f"{low_stock} suku cadang perlu restock", "description": "Periksa inventory sebelum stok habis."})
    if old_waiting:
        insights.append({"type": "waiting_services", "tone": "rose", "title": f"{old_waiting} servis menunggu lebih dari 2 hari", "description": "Prioritaskan follow-up pelanggan."})
    if not insights:
        insights.append({"type": "healthy", "tone": "emerald", "title": "Operasional terlihat sehat", "description": "Belum ada hal penting yang perlu ditindaklanjuti."})
    return {"insights": insights}