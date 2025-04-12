# app/schemas/product.py

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# === 共用欄位 ===
# app/schemas/product.py

from typing import Optional, List
from pydantic import BaseModel

class ProductBase(BaseModel):
    # === 基本資訊 ===
    
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stall_name: Optional[str] = None

    # === 額外資訊 ===
    custom_type: Optional[str] = None          # 自定分類（例如：洋裝）
    material: Optional[str] = None             # 材質
    size_note: Optional[str] = None            # 尺寸描述（可預設帶入）
    real_stock: Optional[int] = None           # 真實庫存
    item_status: Optional[str] = None          # 狀態（待選、已選）

    # === 圖片與資料夾 ===
    image_dir: Optional[str] = None            # 相對圖片路徑（如 A001/001_涼感褲）
    selected_images: Optional[List[str]] = []  # 勾選的圖片
    main_image: Optional[str] = None           # 主圖（如 1.jpg）

    # === 規格資料 ===
    colors: Optional[List[str]] = []
    sizes: Optional[List[str]] = []

    # === Shopee 上傳欄位（自動處理） ===
    shopee_category_id: Optional[int] = None
    min_purchase_qty: Optional[int] = 1
    preparation_days: Optional[int] = None
    logistics_options: Optional[List[str]] = []

    
# === 建立用 ===
class ProductCreate(ProductBase):
    pass

 
# === 回傳資料用（含 ID 與時間） ===

class ProductInDB(ProductBase):
    id: int 
    image_list: Optional[List[dict]] = []
    
    shopee_item_id: Optional[str] = None
    created_at: Optional[datetime] = None 
    updated_at: Optional[datetime] = None 

    class Config:
        from_attributes = True  # pydantic v2: 允許從 ORM 模型轉換
