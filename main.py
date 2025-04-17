import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.utils.config import PRODUCTS_ROOT, CANDIDATES_ROOT
from app.utils.db import Base, engine
from app import models
from app.api.product_routes import product_router 
from app.api.export_routes import export_router
from app.api.admin_page_routes import admin_page_router
from app.api.admin_data_routes import admin_router
from app.utils.config import CANDIDATES_ROOT
app = FastAPI(
    title="Shopee 自動上架系統",
    openapi_tags=[
        {"name": "products", "description": "商品管理 API"},
        {"name": "export", "description": "輸出批次excel檔案"},
    ]
)

from fastapi.staticfiles import StaticFiles
 

# 1️⃣ 網頁使用的靜態資源（JS, CSS, Bootstrap）
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# 2️⃣ 圖片目錄（來自 candidates_root）    
app.mount("/candidate_images", StaticFiles(directory=CANDIDATES_ROOT), name="static")
app.mount("/products_root", StaticFiles(directory=PRODUCTS_ROOT), name="static")


app.mount("/js", StaticFiles(directory="app/static/js"), name="js")
 
# === 模板引擎設定（Jinja2） ===
templates = Jinja2Templates(directory="app/templates")

app.include_router(product_router)
app.include_router(export_router)
app.include_router(admin_page_router)
app.include_router(admin_router)

# 自動建立資料表
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Shopee 上架系統 API 已啟動"}

 