# 📁 app/services/image_storage/image_storage_base.py

import os
from typing import Protocol
from fastapi import UploadFile
from app.models import Product
from app.utils.config import IMAGE_STORAGE_BACKEND


# -------------------------------
# 抽象介面：所有儲存策略需實作
# -------------------------------
class BaseImageService(Protocol):
    async def save_file(self, file: UploadFile, product: Product, file_name : str) -> str:
        """
        儲存單張圖片，回傳圖片的相對路徑（local_path）。
        例如：A001/001_涼感褲/main.jpg
        """
        ...

    def delete_file(self, product: Product, file_name : str) -> str:
        """
        根據儲存的相對路徑刪除圖片檔案。
        回傳是否成功。
        """
        ...

    def get_image_url(self, product: Product, file_name : str) -> str:
        """
        根據相對路徑組合圖片的公開網址。
        可支援本地路徑或雲端圖片 CDN。
        """
        ...


# -------------------------------
# Provider：讀取 .env 決定實例
# -------------------------------
def get_image_service() -> BaseImageService:
    backend = IMAGE_STORAGE_BACKEND
    if backend == "r2":
        # from app.services.image_storage.r2_storage import R2ImageStorage
        # return R2ImageStorage()
        return None
    else:
        from app.services.image_service.local_image_service import LocalImageService
        return LocalImageService()
