from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class ProductQueryParams(BaseModel):
    from_date: Optional[date] = Field(None, description="從此日期開始建立的商品")
    stall: Optional[str] = Field(None, description="檔口名稱模糊比對")
    status: Optional[str] = Field(None, description="商品狀態 (candidate/product/ignore)")
    id: Optional[int] = Field(None, description="商品 ID 精準比對")
    name: Optional[str] = Field(None, description="商品名稱模糊比對")
