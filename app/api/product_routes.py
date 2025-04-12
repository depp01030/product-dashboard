# app/routes/product_routes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.utils.db import SessionLocal
from app.schemas.product import ProductCreate, ProductInDB
from app.services.product_service import (
    create_product, get_all_products, get_product,
    update_product, delete_product
)
from app.utils.image_tools import get_product_images  # 確保你有這個工具函式

product_router = APIRouter(
    prefix="/products",
    tags=["products"]
)

# === Dependency：建立 DB session ===
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# === 建立商品 ===
@product_router.post("/", response_model=ProductInDB)
def create(product: ProductCreate, db: Session = Depends(get_db)):
    return create_product(db, product)

# === 取得所有商品 ===
@product_router.get("/", response_model=List[ProductInDB])
def read_all(db: Session = Depends(get_db)):
    return get_all_products(db)

# === 取得單一商品 ===
@product_router.get("/{product_id}", response_model=ProductInDB)
def read_one(product_id: int, db: Session = Depends(get_db)):
    product = get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# === 預覽圖片清單（回傳本機圖片路徑清單） ===
@product_router.get("/{product_id}/images", response_model=List[str])
def preview_images(product_id: int, db: Session = Depends(get_db)):
    product = get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    image_paths = get_product_images(product)
    return image_paths

# === 更新商品 ===
@product_router.put("/{product_id}", response_model=ProductInDB)
def update(product_id: int, update_data: ProductCreate, db: Session = Depends(get_db)):
    product = update_product(db, product_id, update_data)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# === 刪除商品 ===
@product_router.delete("/{product_id}")
def delete(product_id: int, db: Session = Depends(get_db)):
    product = delete_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted"}

