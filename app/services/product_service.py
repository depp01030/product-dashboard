import os
import json
import shutil
from fastapi import UploadFile, File
from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate, ProductInDB, ProductQuery
from typing import Optional, List
from app.utils.path_tools import init_item_folder, get_abs_folder_path
from app.services.image_service import save_uploaded_images
# === 建立商品 ===

def create_product(db: Session, product_data: ProductCreate, image_import: list[UploadFile] = []) -> Product:
    # 🌀 先轉成 dict，方便我們後面操作
    data = product_data.model_dump()
    print(image_import)
    # ✅ 自動補上 item_folder，如果沒給的話
    if not data.get("item_folder"):
        item_folder = init_item_folder(data['stall_name'], data['name'])
        data["item_folder"] = item_folder
    # 圖片儲存與 selected_images 更新
    print("image_import", image_import)
    if image_import:
        saved_filenames = save_uploaded_images(data["item_folder"], image_import)

        current_names = []
        selected_images = list(set(current_names + saved_filenames))
        data["selected_images"] = selected_images

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

# === 刪除商品 ===
def delete_product(db: Session, product_id: int):
    '''
    刪除商品
        前端會刪除商品卡片，這裡會刪除ｄｂ
        如果這時stall_name有值，則會刪除對應的資料夾
    '''
    product = get_product(db, product_id)
    if product is None:
        return None
    if (product.stall_name != "" and product.stall_name is not None) and \
        (product.item_folder != "" and product.item_folder is not None):
        # 刪除資料夾
        if os.path.exists(get_abs_folder_path(product.item_folder)):
            shutil.rmtree(get_abs_folder_path(product.item_folder))
    db.delete(product)
    db.commit()
    return product

# === 更新商品 ===
def update_product(db: Session, product_id: int, update_data: ProductUpdate, image_import: list[UploadFile] = []):
    '''
    更新產品主服務（不論是哪個 route 進來的）

    關於 item_folder 的更新：
        建立時會自動生成 item_folder（檔口/商品名稱）
        如果更新時的 item_folder 為空，則會保持不變
        如果更新時，stall_name or name 有變更，則會自動生成新的 item_folder
        且還會把原本的 folder 資料完全搬到新 folder，並刪除原本的 folder

    關於圖片處理：
        如果 image_import 中有圖片，則會將圖片存入 item_folder 並更新 selected_images
    '''
    product = get_product(db, product_id)
    if product is None:
        return None

    # item_folder 的更新邏輯
    if (not update_data.item_folder) or \
        (product.stall_name != update_data.stall_name) or \
        (product.name != update_data.name):
        # 生成新的資料夾
        new_item_folder = init_item_folder(update_data.stall_name, update_data.name)
        update_data.item_folder = new_item_folder
        old_item_folder = product.item_folder 
        # 先刪除舊資料夾
        if old_item_folder and old_item_folder != new_item_folder:
            old_item_path = get_abs_folder_path(product.item_folder)
            new_item_path = get_abs_folder_path(update_data.item_folder)

            if os.path.exists(old_item_path):
                # 1. 把舊資料夾的內容搬到新資料夾
                for filename in os.listdir(old_item_path):
                    src_path = os.path.join(old_item_path, filename)
                    dst_path = os.path.join(new_item_path, filename)
                    shutil.move(src_path, dst_path)
                if product.stall_name:
                    # 2. 刪除舊資料夾
                    shutil.rmtree(old_item_path)

    # 圖片儲存與 selected_images 更新
    if image_import:
        saved_filenames = save_uploaded_images(update_data.item_folder, image_import)

        current_names = product.selected_images or []
        update_data.selected_images = list(set(current_names + saved_filenames))

    # 更新欄位
    for key, value in update_data.model_dump().items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product
