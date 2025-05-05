# 📁 app/models/product_image.py

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.sql import func
from app.utils.db import Base

class ProductImage(Base):
    __tablename__ = "product_images"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    file_name = Column(String(255), nullable=False)              # 檔名（不含路徑）
    
    ## 下面兩個，統一透過ImageService 根據不同情境來組成
    # local_path = Column(String(255), nullable=False)            # 本地儲存路徑
    # url = Column(String(255), nullable=True)                    # 外部網址（如果有上傳到 CDN）
    


    is_main = Column(Boolean, default=False)
    is_selected = Column(Boolean, default=False)

    created_at = Column(DateTime, server_default=func.now())

    product = relationship("Product", back_populates="images")
