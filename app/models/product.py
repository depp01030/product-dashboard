# app/models/product.py

from sqlalchemy import Column, Integer, String, Text, DECIMAL, DateTime, JSON
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.sql import func
from app.models.enums import ItemStatusEnum, LogisticsOptionEnum, CustomTypeEnum, SizeMetricsEnum
from app.utils.db import Base

'''
💰 金額類（單位：元）
price：售價：商品最終銷售價格，平台上的售出金額。

purchase_price：訂購價：從檔口或供應商訂購時的單件價格。

intl_shipping_fee：國際運費：從國外寄來台灣的實際運費成本。

customs_duty：關稅：進口商品時需繳納的關稅金額。

exchange_rate：匯率：將外幣換算為台幣所使用的匯率（如 4.38）。

stock_cost：進貨成本：一件商品從海外採購到抵台完成備貨的實際總成本。

listing_cost：上架成本：每件商品在平台上架所花費的費用（如服務費、處理費）。

total_cost：總成本：包含所有成本項目的加總（進貨成本 + 關稅 + 上架等）。

📐 比例類（單位：0 ~ 1 的比例）
shipping_ratio：貨運費比例：貨運費占訂購價的比例，例如 0.2 表示佔 20%。

listing_ratio：上架費比例：平台上架費用占售價的比例，例如 0.1 表示佔 10%。



'''

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True) 

    # === 基本資訊 ===
    name = Column(String(255), nullable=True)               # 商品名稱
    description = Column(Text, nullable=True)               # 商品描述

    purchase_price = Column(DECIMAL(10, 2), nullable=True)  # 訂購價(韓元)
    total_cost = Column(DECIMAL(10, 2), nullable=True)      # 總成本
    price = Column(DECIMAL(10, 2), nullable=True)           # 價格


    stall_name = Column(String(100), nullable=True)         # 檔口名稱
    source = Column(String(255), nullable=True)             # 來源
    source_url = Column(String(255), nullable=True)         # 網站連結
    item_status = Column(SQLEnum(ItemStatusEnum), 
                         default=ItemStatusEnum.product, nullable=True)  # 商品狀態
    

    # === 類別與規格資訊 ===
    custom_type = Column(SQLEnum(CustomTypeEnum),
                        nullable=True)                         # 自定分類（例如：洋裝）
    material = Column(String(255), nullable=True)              # 材質
    size_metrics = Column(JSON, nullable=True)                 # 尺寸資訊 {"shoulder": "40", "length": "65"}
    size_note = Column(Text, nullable=True)                    # 尺寸額外描述
    real_stock = Column(Integer, nullable=True)                # 真實庫存

    # === 圖片管理 ===
    item_folder = Column(String(255))                        # 相對資料夾路徑(產品主資料夾）（例如：A001/001_涼感褲）
    main_image = Column(String(255), nullable=True)          # 主圖片檔名（例如：1.jpg）
    image_name_list = Column(JSON, nullable=True)            # 圖片列表（["1.jpg", "2.jpg"]）

    # === 商品分類與設定 ===
    shopee_category_id = Column(Integer, nullable=True)     # Shopee 類別 ID（純數字）
    min_purchase_qty = Column(Integer, default=1)           # 最低購買數量
    preparation_days = Column(Integer, default=30)          # 較長備貨天數（例如：30）

    # === 規格資訊 ===
    colors = Column(JSON, nullable=True)                    # 可選顏色（["白", "藍", "紅"]）
    sizes = Column(JSON, nullable=True)                     # 可選尺寸（["M", "L", "XL"]）

    # === 配送方式 ===
    logistics_options = Column(
                    JSON,
                    nullable=True,
                    default=[LogisticsOptionEnum.shopee_store_pickup.value,
                             LogisticsOptionEnum.seven_eleven.value,
                             LogisticsOptionEnum.hilife.value,
                             LogisticsOptionEnum.familymart.value,]  
                )        # 配送方案（["7-ELEVEN", "全家"]）

    # === 時間戳 ===
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
