# app/schemas/product.py

from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel, field_validator
from datetime import datetime
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
    image_dir: Optional[str] = None            
    selected_images: List[str] = []  
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

    @field_validator('selected_images', 'colors', 'sizes', 'logistics_options', mode='before')
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

class ProductCreate(ProductBase):
    pass

class ProductInDB(ProductBase):
    id: int 
    image_list: Optional[List[dict]] = []
    shopee_item_id: Optional[str] = None
    created_at: Optional[datetime] = None 
    updated_at: Optional[datetime] = None 

    class Config:
        from_attributes = True
