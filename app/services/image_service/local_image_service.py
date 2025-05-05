# 📁 app/services/image_service/local_image_service.py

from pathlib import Path
from fastapi import UploadFile
from uuid import uuid4
import os

from app.models.product import Product
from app.services.image_service.base_image_service import BaseImageService
from app.utils.config import IMAGE_LOCAL_BASE_DIR, IMAGE_URL_BASE


class LocalImageService(BaseImageService):
    def __init__(self):
        self.base_dir = Path(IMAGE_LOCAL_BASE_DIR)


    async def save_file(self, file: UploadFile, product: Product, file_name: str) -> str:
        """
        儲存圖片，回傳圖片相對路徑（相對於 base_dir）。

        - 實際儲存路徑為：{base_dir}/{stall_name}/{product_name}/{file_name}
        - 適用於自訂檔名或保留原始檔名（由呼叫端控制 file_name 內容）
        """
        # 組成儲存資料夾路徑 
        folder = os.path.join(self.base_dir, product.stall_name, product.name)
        os.makedirs(folder, exist_ok=True)

        # 若檔名沒有副檔名，補上 .jpg
        _, ext = os.path.splitext(file_name)
        if not ext:
            file_name += ".jpg"

        # 組成完整儲存路徑
        full_path = os.path.join(folder, file_name)

        # 寫入檔案
        content = await file.read()
        with open(full_path, "wb") as f:
            f.write(content)

        # 回傳相對於 base_dir 的路徑（例如 A001/001_涼感褲/main.jpg）
        rel_path = os.path.relpath(full_path, self.base_dir)
        return rel_path

    def delete_file(self, product: Product, file_name: str) -> bool:
        """
        根據 product 與 file_name 組出完整路徑，刪除圖片。
        """
        path = self.base_dir / product.stall_name / product.name / file_name
        try:
            if path.exists():
                path.unlink()
            return True
        except Exception:
            return False

    def get_image_url(self, product: Product, file_name: str) -> str:
        """
        根據 product 與檔名組出完整公開 URL。
        """
        return f"{IMAGE_URL_BASE}/{product.stall_name}/{product.name}/{file_name}"
