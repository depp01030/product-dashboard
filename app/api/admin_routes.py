# app/routes/admin_routes.py

from fastapi import APIRouter, Request, Depends, Form, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta

from app.utils.db import get_db
from app.utils.template_engine import templates
from app.constants.status_labels import STATUS_LABELS

from app.models.product import Product
from app.schemas.product import ProductInDB
from app.schemas.product_update_form import ProductUpdateForm
from app.schemas.product_query import ProductQueryParams
from app.services.product_service import (
    update_product_by_dict,
    query_products_with_filters
)
from app.services.import_service import (
    import_candidates_from_folder
)
from app.utils.image_tools import (
    get_admin_product_image_info_list
)

admin_router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)

@admin_router.post("/import-candidates")
def trigger_import_candidates():
    count = import_candidates_from_folder()
    return {"message": f"成功匯入 {count} 筆資料"}
# === 頁面：僅回傳 HTML 框架 ===
@admin_router.get("/products", response_class=HTMLResponse)
def show_product_list(request: Request):
    return templates.TemplateResponse("admin/products.html", {
        "request": request,
        "candidate_images_prefix": "/candidate_images/",
        "status_labels": STATUS_LABELS
    })

# === API：支援篩選 + 分頁 ===
@admin_router.get("/api/products/search", response_model=List[ProductInDB])
def get_product_list_with_filter(
    db: Session = Depends(get_db), 
    params: ProductQueryParams = Depends(),
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100)
):
    products = query_products_with_filters(db, params, offset=offset, limit=limit)

    for p in products:
        p.selected_images = p.selected_images or []
        p.image_list = get_admin_product_image_info_list(p.image_dir)

    return products

# === API：單純分頁（無篩選）===
@admin_router.get("/api/products", response_model=List[ProductInDB])
def get_product_list_json(
    db: Session = Depends(get_db),
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100)
):
    products = db.query(Product).order_by(Product.created_at.desc()).offset(offset).limit(limit).all()

    for p in products:
        p.selected_images = p.selected_images or []
        p.image_list = get_admin_product_image_info_list(p.image_dir)

    return products

# === 更新商品資料 ===
@admin_router.post("/products/{product_id}/update")
def update_product_from_admin(
    product_id: int,
    form: ProductUpdateForm = Depends(),
    db: Session = Depends(get_db)
): 
    update_product_by_dict(db, product_id, form.__dict__)
    return RedirectResponse(url="/admin/products", status_code=303)
