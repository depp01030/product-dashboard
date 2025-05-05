# 📁 app/schemas/product_image.py

from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime


# --------------------------------------------------------
# ✅ 共用欄位：提供給各種用途繼承
# --------------------------------------------------------

class ProductImageBase(BaseModel):
    product_id: int                             # 關聯商品 ID
    file_name: Optional[str] = None             # 檔名（僅供前端顯示用）
    is_main: Optional[bool] = False             # 是否為主圖
    is_selected: Optional[bool] = False         # 是否選取


# --------------------------------------------------------
# 🆕 建立圖片 metadata 用（目前未使用，保留作為 interface stub）
# --------------------------------------------------------

class ProductImageCreate(BaseModel):
    pass


# --------------------------------------------------------
# 📤 回傳給前端用（例如 GET /product-image/product/{id}）
# --------------------------------------------------------

class ProcessedImageInfo(ProductImageBase):
    id: int                                     # 資料庫內部 ID
    url: Optional[str] = None                   # 公開預覽網址（或 objectURL）

    created_at: Optional[datetime] = None       # 建立時間
    updated_at: Optional[datetime] = None       # 更新時間

    class Config:
        from_attributes = True


# --------------------------------------------------------
# 📥 提交給後端用（例如 POST /process 時送出的 metadata）
# --------------------------------------------------------

class ProductImageSubmission(BaseModel):
    id: Optional[int] = None                    # 舊圖才有
    temp_id: Optional[str] = None               # 前端臨時 UUID，僅新圖使用
    action: Literal['original', 'new', 'update', 'delete'] = 'original'
    is_main: bool                               # 是否主圖
    is_selected: bool                           # 是否選取
 