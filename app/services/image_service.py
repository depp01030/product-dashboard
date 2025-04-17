import os
import shutil
from datetime import datetime
from typing import List

from fastapi import UploadFile, HTTPException

from app.utils.config import PRODUCTS_ROOT  
from app.utils.path_tools import get_abs_folder_path

__all__ = [
    "ALLOWED_IMAGE_EXTENSIONS",
    "get_abs_folder_path",
    "save_uploaded_images",
]

# ================================
# 允許的圖片副檔名
# ================================
ALLOWED_IMAGE_EXTENSIONS: set[str] = {".jpg", ".jpeg", ".png"}

# ================================
# 公用工具
# ================================
 


# ================================
# 主要服務：儲存上傳圖片
# ================================

def save_uploaded_images(item_folder: str, files: List[UploadFile]) -> List[str]:
    """將上傳的圖片儲存到指定 item_folder，並回傳實際儲存的檔名列表。

    - 同名檔案會自動在檔名後加時間戳避免覆蓋。
    - 只有 `ALLOWED_IMAGE_EXTENSIONS` 中允許的副檔名會被接受。
    """

    if not files:
        return []

    abs_folder = get_abs_folder_path(item_folder)

    saved_filenames: list[str] = [] 
    for upload in files:
        # 1️⃣ 副檔名檢查
        ext = os.path.splitext(upload.filename)[1].lower()
        if ext not in ALLOWED_IMAGE_EXTENSIONS:
            continue

        # 2️⃣ 檔名處理（加時間戳）
        base_name = os.path.splitext(upload.filename)[0]
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        safe_filename = f"{base_name}_{timestamp}{ext}"
        save_path = os.path.join(abs_folder, safe_filename)

        # 3️⃣ 寫入硬碟
        with open(save_path, "wb") as f:
            shutil.copyfileobj(upload.file, f)

        saved_filenames.append(safe_filename)

    return saved_filenames
