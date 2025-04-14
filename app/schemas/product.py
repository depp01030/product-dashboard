# app/schemas/product.py

from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel, Field, field_validator
from datetime import datetime, date
import json

class ProductBase(BaseModel):
    # === 基本資訊 ===
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stall_name: Optional[str] = None
    source: Optional[str] = None

    # === 額外資訊 ===
    custom_type: Optional[str] = None          
    material: Optional[str] = None             
    size_metrics: Dict[str, str] = {}    # Changed from Optional[Dict] to Dict with default
    size_note: Optional[str] = None            
    real_stock: Optional[int] = None           
    item_status: Optional[str] = None          

    # === 圖片與資料夾 ===
    item_folder: Optional[str] = None       
    main_image: Optional[str] = None           

    # === 規格資料 ===
    colors: List[str] = []
    sizes: List[str] = []

    # === Shopee 上傳欄位 ===
    shopee_category_id: Optional[int] = None
    min_purchase_qty: Optional[int] = 1
    preparation_days: Optional[int] = None
    logistics_options: List[str] = []

    @field_validator('size_metrics', mode='before')
    @classmethod
    def ensure_dict_size_metrics(cls, value: Any) -> Dict[str, str]:
        if value is None:
            return {}
        if isinstance(value, dict):
            return value
        if isinstance(value, str):
            try:
                parsed = json.loads(value)
                return parsed if isinstance(parsed, dict) else {}
            except json.JSONDecodeError:
                return {}
        return {}

    @field_validator('colors', 'sizes', 'logistics_options', mode='before')
    @classmethod
    def ensure_list_fields(cls, value: Any) -> List[str]:
        if value is None:
            return []
        if isinstance(value, list):
            return value
        if isinstance(value, str):
            try:
                parsed = json.loads(value)
                return parsed if isinstance(parsed, list) else []
            except json.JSONDecodeError:
                return []
        return []

class ProductQuery(ProductBase):
    id: Optional[int] = Field(None, description="商品 ID 精準比對")
    name: Optional[str] = Field(None, description="商品名稱模糊比對")
    item_status: Optional[str] = Field(None, description="商品狀態 (candidate/product/ignore)")
    stall: Optional[str] = Field(None, description="檔口名稱模糊比對")
    from_date: Optional[date] = Field(None, description="從此日期開始建立的商品")

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass
class ProductInDB(ProductBase):
    id: int 
    image_list: Optional[List[dict]] = []
    shopee_item_id: Optional[str] = None
    created_at: Optional[datetime] = None 
    updated_at: Optional[datetime] = None 

    class Config:
        from_attributes = True
