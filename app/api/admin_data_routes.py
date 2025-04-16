# 📁 app/api/admin_data_routes.py
from fastapi import APIRouter, Request, Depends, Form, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta

from app.utils.db import get_db
from app.utils.template_engine import templates
from app.constants.status_labels import STATUS_LABELS
 
from app.models.product import Product
from app.schemas.product import ProductInDB, ProductUpdate, ProductCreate, ProductQuery
from app.schemas.product_update_form import ProductUpdateForm 
from app.services.product_service import (
    create_product,
    update_product,
    delete_product,
    query_products_with_filters
)
from app.services.import_service import import_candidates_from_folder
from app.utils.image_tools import get_admin_product_image_info_list

admin_router = APIRouter(prefix="/admin", tags=["admin_data"])

# # === ✅ 匯入候選商品 ===
# @admin_router.post("/import-candidates")
# def trigger_import_candidates():
#     count = import_candidates_from_folder()
#     return {"message": f"成功匯入 {count} 筆資料"}

# === ✅ 查詢商品（可帶參數篩選） ===
@admin_router.get("/api/products", response_model=List[ProductInDB])
def get_product_list_with_filter(
    db: Session = Depends(get_db),
    params: ProductQuery = Depends(),
    offset: int = Query(0, ge=0),
    limit: int = Query(100, le=200)
): 
    products = query_products_with_filters(db, params, offset=offset, limit=limit)
    for p in products: 
        p.image_list = get_admin_product_image_info_list(p.item_folder)

    return products


# === ✅ 建立商品 ===
@admin_router.post("/products/create")
def create_product_from_admin(
    form: ProductUpdateForm = Depends(),
    db: Session = Depends(get_db)
):
    product = ProductCreate(**form.__dict__)
    product = create_product(db, product)
    return product #RedirectResponse(url="/admin/products", status_code=303)

# === ✅ 提交商品編輯表單 ===
@admin_router.post("/products/{product_id}/update")
def update_product_from_admin(
    product_id: int,
    form: ProductUpdateForm = Depends(),
    db: Session = Depends(get_db)
):
    product = ProductUpdate(**form.__dict__) 
    update_product(db, product_id, product)
    return #RedirectResponse(url="/admin/products", status_code=303)

@admin_router.delete("/products/{product_id}/delete")
def delete_product_from_admin(product_id: int, db: Session = Depends(get_db)):
    delete_product(db, product_id)
    return  
