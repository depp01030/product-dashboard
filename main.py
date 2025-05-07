
# main.py
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from app.utils.config import PRODUCTS_ROOT, IMAGE_LOCAL_BASE_URL
from app.utils.db import Base, engine

from fastapi import FastAPI
from app.api.admin import products 
from app.api.admin import product_images 
from app.api import auth
from app.api import health
app = FastAPI(
    title="Shopee 自動上架系統",
    openapi_tags=[
        {"name": "products", "description": "商品管理 API"},
     ]
) 

# 添加 CORS 中間件
app.add_middleware(
    CORSMiddleware,
    allow_origins = [
        "https://herstudio-admin-react.vercel.app",  # 前端的正式網址
        "http://localhost:5173",  # 開發測試用
        "http://localhost:4173",  # 開發測試用
    ],
    allow_credentials=True,
    allow_methods=["*"],  # 允許所有 HTTP 方法
    allow_headers=["*"],  # 允許所有 headers
)


# 指定根資料夾路徑（你自己改）
from app.utils.config import PRODUCTS_ROOT  # 或直接寫 "./Candidates_root"

app.mount(IMAGE_LOCAL_BASE_URL, StaticFiles(directory=PRODUCTS_ROOT), name="images")

# 依功能註冊 router
app.include_router(health.router)
app.include_router(auth.router)
app.include_router(product_images.router)
app.include_router(products.router)
# app.include_router(product_images.router, prefix="/api/admin/products/{product_id}/images", tags=["Product Images"])
# app.include_router(auth.router, prefix="/api/admin/auth", tags=["Auth"])


# 自動建立資料表
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return Response(content="你好，世界", media_type="text/plain; charset=utf-8")

from sqlalchemy import text 
from app.utils.db import SessionLocal

@app.on_event("startup")
def test_db_connection():
    try:
        with SessionLocal() as session:
            session.execute(text("SELECT 1"))
        print("✅ 成功連線到資料庫")
    except Exception as e:
        print("❌ 無法連線資料庫：", e)