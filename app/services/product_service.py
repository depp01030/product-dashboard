import os
import json
from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate, ProductInDB, ProductQuery
from typing import Optional, List
from app.utils.path_tools import init_item_folder
# === 建立商品 ===

def create_product(db: Session, product_data: ProductCreate) -> Product:
    # 🌀 先轉成 dict，方便我們後面操作
    data = product_data.model_dump()
    
    # ✅ 自動補上 item_folder，如果沒給的話
    if not data.get("item_folder"):
        item_folder = init_item_folder(data['stall_name'], data['name'])
        data["item_folder"] = item_folder

    # ✅ 寫入資料庫
    db_product = Product(**data)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product
# === 取得所有商品 ===
def get_all_products(db: Session):
    return db.query(Product).all()

# === 取得單一商品 ===
def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

# app/services/product_service.py

def query_products_with_filters(
    db: Session,
    params: ProductQuery,
    offset: int = 0,
    limit: Optional[int] = None
) -> List[Product]:
    query = db.query(Product)

    # 起始時間（created_at）
    if params.from_date:
        query = query.filter(Product.created_at >= params.from_date)

    # 檔口模糊比對（支援 * 通配）
    if params.stall:
        stall_keyword = params.stall.replace("*", "%")
        query = query.filter(Product.stall_name.like(f"%{stall_keyword}%"))

    # 狀態（完全相等）
    if params.item_status: 
        query = query.filter(Product.item_status == params.item_status)

    # ID（完全相等）
    if params.id:
        query = query.filter(Product.id == params.id)
    # website (完全相等）
    if params.source_url:
        query = query.filter(Product.source_url == params.source_url)

    # 商品名稱模糊比對（支援 * 通配）
    if params.name:
        name_keyword = params.name.replace("*", "%")
        query = query.filter(Product.name.like(f"%{name_keyword}%"))

    # 排序
    query = query.order_by(Product.created_at.desc())

    # 分頁（可選）
    if limit is not None:
        query = query.offset(offset).limit(limit)

    return query.all()

# === 更新商品 ===
def _update_product_by_dict(db: Session, product_id: int, update_data: dict):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return None
        
    for key, value in update_data.items():
        if key == 'size_metrics':
            # 特殊處理 size_metrics，確保它是一個有效的 JSON 字典
            if isinstance(value, dict):
                value = json.dumps(value)
            elif isinstance(value, str):
                try:
                    parsed = json.loads(value)
                    if not isinstance(parsed, dict):
                        value = '{}'
                except json.JSONDecodeError:
                    value = '{}'
        elif key in ['colors', 'sizes', 'logistics_options']:
            # 處理其他 JSON 列表欄位
            if isinstance(value, (list, dict)):
                value = json.dumps(value)
            elif isinstance(value, str):
                try:
                    json.loads(value)  # 驗證 JSON 格式
                except json.JSONDecodeError:
                    value = '[]'
        elif isinstance(value, str) and value.strip().lower() == "none":
            value = None
            
        setattr(product, key, value)
        
    db.commit()
    db.refresh(product)
    return product

def update_product(db: Session, product_id: int, update_data: ProductUpdate):
    product = get_product(db, product_id)
    if product is None:
        return None
    for key, value in update_data.model_dump().items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product

# === 刪除商品 ===
def delete_product(db: Session, product_id: int):
    product = get_product(db, product_id)
    if product is None:
        return None
    db.delete(product)
    db.commit()
    return product
