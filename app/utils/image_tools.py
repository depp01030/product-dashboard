# app/utils/image_tools.py
import os
from urllib.parse import quote  
from pathlib import Path
from typing import List, Optional
from app.utils.config import get_candidates_root
from app.models.product import Product

import os
from typing import List, Optional
from urllib.parse import quote

from app.utils.config import load_env 

load_env()

CANDIDATES_ROOT = os.getenv("CANDIDATES_ROOT")
def _get_sorted_images(image_dir: str) -> List[str]:
    '''
    image_dir = "bronze/9 高品質內磨毛水洗牛仔褲 SM 1194 1780"
    '''
    abs_path = os.path.join(CANDIDATES_ROOT, image_dir)
    if not os.path.isdir(abs_path):
        return []
    return sorted(
        f for f in os.listdir(abs_path)
        if f.lower().endswith(('.jpg', '.jpeg', '.png'))
    )

def get_images_url(image_dir: str, limit: int = 8) -> List[str]:
    """
    根據環境變數 USE_IMAGE_URL 決定回傳本地路徑或網址路徑
    """
    files = _get_sorted_images(image_dir)[:limit]
    image_paths = []

    use_url = os.getenv("USE_IMAGE_URL", "false").lower() == "true"
    base_url = os.getenv("IMAGE_URL_BASE", "")

    for file in files:
        if use_url:
            rel_path = f"{image_dir}/{file}".replace("\\", "/")
            encoded_path = quote(rel_path)
            image_paths.append(f"{base_url}/{encoded_path}")
        else:
            abs_path = os.path.join(CANDIDATES_ROOT, image_dir, file)
            image_paths.append(abs_path)

    return image_paths

def get_admin_product_image_info_list(image_dir: str) -> Optional[str]:
    """
    回傳image_info :{
        "image_url": "/candidate_images/xxx.jpg",
        "filename": "xxx.jpg"
    }
    為了讓前端可以顯示與篩選
    """
    filenames = _get_sorted_images(image_dir)
    use_url = os.getenv("USE_IMAGE_URL", "false").lower() == "true"
    base_url = os.getenv("IMAGE_URL_BASE", "")

    result = []
    for filename in filenames:
        rel_path = f"{image_dir}/{filename}".replace("\\", "/")
        encoded_path = quote(rel_path)
        result.append({
            "filename": filename,
            "url": encoded_path
        })
    return result
def get_main_image_url(image_dir: str) -> Optional[str]:
    """
    回傳第一張圖片的網址（不考慮本地路徑，只給後台顯示用）
    """
    files = _get_sorted_images(image_dir)
    if not files:
        return None

    rel_path = f"{image_dir}/{files[0]}".replace("\\", "/")
    encoded_path = quote(rel_path)
    return f"/candidate_images/{encoded_path}"

def get_main_image_path(image_dir: str) -> Optional[str]:
    """
    回傳第一張圖片的網址（不考慮本地路徑，只給後台顯示用）
    """
    files = _get_sorted_images(image_dir)
    if not files:
        return None

    rel_path = f"{image_dir}/{files[0]}".replace("\\", "/")
    return f"/candidate_images/{rel_path}"

def get_product_images(product: Product) -> List[str]:
    """
    傳回指定 product 對應的所有圖片絕對路徑
    """
    root = Path(get_candidates_root())
    folder = root / product.image_dir

    if not folder.exists() or not folder.is_dir():
        return []

    image_files = sorted([
        str(p.resolve()) for p in folder.glob("*")
        if p.suffix.lower() in [".jpg", ".jpeg", ".png", ".webp"]
    ])
    return image_files

