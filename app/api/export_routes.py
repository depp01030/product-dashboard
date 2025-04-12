# app/routes/export_routes.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.utils.db import SessionLocal
from app.services.product_service import get_all_products
from app.exporter.shopee_excel_exporter import export_products_to_excel

export_router = APIRouter(
    prefix="/export",
    tags=["export"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@export_router.get("/shopee")
def export_excel(db: Session = Depends(get_db)):
    products = get_all_products(db)
    path = export_products_to_excel(products)
    return {"exported_file": path}
