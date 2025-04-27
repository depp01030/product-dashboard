# app/services/product_service.py
"""
商品 Service  ── 專責商業邏輯，不處理 FastAPI 相關細節
"""

from __future__ import annotations

from typing import List, Tuple

from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductQueryParams,
    ProductQuery,
    ProductInDB,
)
from app.schemas.pagination import PaginatedProducts
from app.services.product_service_logic import (
    query_products_with_filters,  # 你先前的查詢工具函式
)
from app.utils.image_tools import get_admin_product_image_info_list


# ────────────────────────────────────────────────────────────────────
# 查 詢
# ────────────────────────────────────────────────────────────────────
def get_products(db: Session, params: ProductQueryParams) -> PaginatedProducts:
    """依傳入條件分頁取得商品清單"""

    # 1. 轉換 QueryParams → 原 query_products_with_filters 需要的 ProductQuery


    # 2. 先算 total（不分頁）
    total_items: List[Product] = query_products_with_filters(
        db, params, offset=0, limit=None
    )
    total = len(total_items)

    # 3. 取得當頁資料
    offset = (params.page - 1) * params.page_size
    page_items: List[Product] = query_products_with_filters(
        db, params, offset=offset, limit=params.page_size
    )

    # 4. 組回傳
    total_pages = (total + params.page_size - 1) // params.page_size
    return PaginatedProducts(
        items=[ProductInDB.from_orm(p) for p in page_items],
        total=total,
        page=params.page,
        page_size=params.page_size,
        total_pages=total_pages,
    )


def get_product_detail(db: Session, product_id: int) -> ProductInDB:
    """取得單一商品詳情；找不到 raise ValueError"""
    product: Product | None = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise ValueError("商品不存在")

    # ➜ 補上圖片清單（若你不想要可刪）
    images = get_admin_product_image_info_list(product_id)
    product_data = ProductInDB.from_orm(product).dict()
    product_data["image_list"] = images
    return ProductInDB(**product_data)


# ────────────────────────────────────────────────────────────────────
# 建 立 / 更 新
# ────────────────────────────────────────────────────────────────────
def create_product(db: Session, data: ProductCreate) -> ProductInDB:
    new_p = Product(**data.dict(exclude_unset=True))
    db.add(new_p)
    db.commit()
    db.refresh(new_p)
    return ProductInDB.from_orm(new_p)


def update_product(db: Session, product_id: int, data: ProductUpdate) -> ProductInDB:
    product: Product | None = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise ValueError("商品不存在")

    for field, value in data.dict(exclude_unset=True).items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)
    return ProductInDB.from_orm(product)


# ────────────────────────────────────────────────────────────────────
# 刪 除
# ────────────────────────────────────────────────────────────────────
def delete_product(db: Session, product_id: int) -> bool:
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return False
    db.delete(product)
    db.commit()
    return True


def batch_delete_products(db: Session, ids: List[int]) -> Tuple[int, List[int]]:
    """回傳 (成功刪除數, 刪除失敗 id 列表)"""
    success_cnt = 0
    failed: List[int] = []

    for pid in ids:
        if delete_product(db, pid):
            success_cnt += 1
        else:
            failed.append(pid)

    return success_cnt, failed
