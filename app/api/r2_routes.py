# 📁 app/api/r2_routes.py
import os
import sys 

from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from app.services.upload_image_service import upload_file_to_r2

from datetime import datetime
from pathlib import Path

from app.utils.config import PRODUCTS_ROOT  

r2_router = APIRouter(prefix="/r2", tags=["r2"])

# === ✅ 單張圖片上傳到 R2，並回傳公開網址 ===
@r2_router.post("/upload-image")
async def upload_image_to_r2(
    file: UploadFile = File(...)
):
    try:
        local_image = Path(os.path.join(PRODUCTS_ROOT,"QrCode.jpg"))

        if not local_image.exists():
            return {"success": False, "error": f"找不到檔案：{local_image}"}

        # R2 中儲存的路徑 key
        key = "test_uploads/QrCode.jpg"

        # 上傳
        url = upload_file_to_r2(local_image, key)
        return {"success": True, "url": url}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )
