# app/services/product_service.py
"""
商品 Service ── 專責商業邏輯
"""
from typing import List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc

from app.models.product import Product
from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductQueryParams,
    ProductInDB,
)
from app.schemas.pagination import PaginatedProducts
from app.utils.image_tools import get_admin_product_image_info_list


# ───────────────────────────────────────────────
# 篩選工具
# ───────────────────────────────────────────────
def filter_products(
    db: Session,
    params: ProductQueryParams
) -> Tuple[List[Product], int]:
    """
    依 ProductQueryParams 組條件，**含分頁**。
    回傳 (當頁商品 list, 總筆數)
    """
    query = db.query(Product)

    # ---- 精準欄位 ---------------------------------------------------
    if params.id is not None:
        query = query.filter(Product.id == params.id)

    if params.source:
        query = query.filter(Product.source.ilike(f"%{params.source}%"))

    # ---- 模糊欄位 ---------------------------------------------------
    if params.name:
        kw = params.name.replace("*", "%")
        query = query.filter(Product.name.ilike(f"%{kw}%"))

    if params.stall:
        kw = params.stall.replace("*", "%")
        query = query.filter(Product.stall_name.ilike(f"%{kw}%"))

    # ---- 日期 -------------------------------------------------------
    if params.from_date:
        query = query.filter(Product.created_at >= params.from_date)

    # ---- 排序 -------------------------------------------------------
    sort_col = getattr(Product, params.sort_by, Product.created_at)
    direction = desc if params.sort_order == "desc" else asc
    query = query.order_by(direction(sort_col))

    # ---- 分頁 -------------------------------------------------------
    total_count = query.count()
    offset = (params.page - 1) * params.page_size
    page_items = query.offset(offset).limit(params.page_size).all()

    return page_items, total_count


# ───────────────────────────────────────────────
# 取得分頁商品清單
# ───────────────────────────────────────────────
def get_products(db: Session, params: ProductQueryParams) -> PaginatedProducts:
    """
    先呼叫 filter_products 取得 (資料, 總筆數)，
    再組成 PaginatedProducts 回傳
    """
    page_items, total = filter_products(db, params)

    total_pages = (total + params.page_size - 1) // params.page_size
    return PaginatedProducts(
        items=[ProductInDB.model_validate(p, from_attributes=True) for p in page_items],
        total=total,
        page=params.page,
        page_size=params.page_size,
        total_pages=total_pages,
    )
def get_product_detail(db: Session, product_id: int) -> ProductInDB:
    """
    取得單一商品詳情；若找不到則 raise ValueError
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise ValueError("商品不存在")

    schema_obj = ProductInDB.model_validate(product, from_attributes=True)
    # schema_obj.image_list = get_admin_product_image_info_list(product_id)
    return schema_obj


# ───────────────────────────────────────────────
# 建立 / 更新
# ───────────────────────────────────────────────
def create_product(db: Session, data: ProductCreate) -> ProductInDB:
    new_product = Product(**data.dict(exclude_unset=True))
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return ProductInDB.model_validate(new_product, from_attributes=True)


def update_product(db: Session, product_id: int, data: ProductUpdate) -> ProductInDB:
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise ValueError("商品不存在")

    for field, value in data.dict(exclude_unset=True).items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)
    return ProductInDB.model_validate(product, from_attributes=True)


# ───────────────────────────────────────────────
# 刪除
# ───────────────────────────────────────────────
def delete_product(db: Session, product_id: int) -> bool:
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        return False
    db.delete(product)
    db.commit()
    return True


def batch_delete_products(db: Session, product_ids: List[int]) -> Tuple[int, List[int]]:
    """回傳 (成功刪除數, 刪除失敗的 product_id 列表)"""
    success_cnt = 0
    failed: List[int] = []

    for product_id in product_ids:
        if delete_product(db, product_id):
            success_cnt += 1
        else:
            failed.append(product_id)

    return success_cnt, failed
