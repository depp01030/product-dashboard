
# main.py
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from app.utils.config import PRODUCTS_ROOT, CANDIDATES_ROOT
from app.utils.db import Base, engine

from fastapi import FastAPI
from api.admin import products, product_images, auth

app = FastAPI(
    title="Shopee 自動上架系統",
    openapi_tags=[
        {"name": "products", "description": "商品管理 API"},
     ]
) 

# 添加 CORS 中間件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # 允許前端地址
    allow_credentials=True,
    allow_methods=["*"],  # 允許所有 HTTP 方法
    allow_headers=["*"],  # 允許所有 headers
)

# 依功能註冊 router
app.include_router(products.router, prefix="/api/admin/products", tags=["Products"])
app.include_router(product_images.router, prefix="/api/admin/products/{product_id}/images", tags=["Product Images"])
app.include_router(auth.router, prefix="/api/admin/auth", tags=["Auth"])


# 自動建立資料表
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Shopee 上架系統 API 已啟動"}

 