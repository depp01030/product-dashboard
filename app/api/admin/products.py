# app/api/admin/products.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from app.utils.db import get_db
from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductQueryParams,
    ProductInDB,
)
from app.schemas.pagination import PaginatedProducts 
from app.services import product_service

router = APIRouter(prefix="/api/admin/products", tags=["Products"])

# --------------------------------------------------------------------
# 1.  商品清單  -------------------------------------------------------
# --------------------------------------------------------------------
@router.get("", response_model=PaginatedProducts) 
async def get_products(
    query: ProductQueryParams = Depends(),
    db: Session = Depends(get_db),
):
    print(query)
    return product_service.get_products(db, query)

# --------------------------------------------------------------------
# 2.  商品詳情  -------------------------------------------------------
# --------------------------------------------------------------------
@router.get("/{product_id}", response_model=ProductInDB)
async def get_product_detail(
    product_id: int,
    db: Session = Depends(get_db),
):
    try:
        return product_service.get_product_detail(db, product_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="商品不存在")

# --------------------------------------------------------------------
# 3.  建立商品  -------------------------------------------------------
# --------------------------------------------------------------------
@router.post("", response_model=ProductInDB, status_code=status.HTTP_201_CREATED)
async def create_new_product(
    data: ProductCreate,
    db: Session = Depends(get_db),
):
    return product_service.create_product(db, data)

# --------------------------------------------------------------------
# 4.  更新商品  -------------------------------------------------------
# --------------------------------------------------------------------
@router.put("/{product_id}", response_model=ProductInDB)
async def update_product_data(
    product_id: int,
    data: ProductUpdate,
    db: Session = Depends(get_db),
):
    try:
        return product_service.update_product(db, product_id, data)
    except ValueError:
        raise HTTPException(status_code=404, detail="商品不存在")

# --------------------------------------------------------------------
# 5.  刪除商品  -------------------------------------------------------
# --------------------------------------------------------------------
@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    if not product_service.delete_product(db, product_id):
        raise HTTPException(status_code=404, detail="商品不存在")
    # 204 No-Content 回傳空 body
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# --------------------------------------------------------------------
# 6.  批次刪除  ------------------------------------------------------
# --------------------------------------------------------------------
@router.post("/batch-delete")
async def batch_delete_products(
    ids: List[int],
    db: Session = Depends(get_db),
):
    success_cnt, failed_ids = product_service.batch_delete_products(db, ids)
    return {
        "total": len(ids),
        "success_count": success_cnt,
        "failed_count": len(failed_ids),
        "failed_ids": failed_ids,
    }
