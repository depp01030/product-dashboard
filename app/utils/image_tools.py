# app/utils/image_tools.py
import os
from urllib.parse import quote  
from pathlib import Path
from typing import List, Optional
from PIL import Image
import io
from app.utils.config import get_candidates_root
from app.models.product import Product
from app.utils.config import load_env 

load_env()

CANDIDATES_ROOT = os.getenv("CANDIDATES_ROOT")

def get_thumbs_path(image_path: str) -> str:
    """
    獲取壓縮圖片的儲存路徑（在 thumbs 資料夾中）
    例如：
    原圖：/path/to/folder/image.jpg
    縮圖：/path/to/folder/thumbs/image.jpg
    """
    dir_path = os.path.dirname(image_path)
    filename = os.path.basename(image_path)
    thumbs_dir = os.path.join(dir_path, "thumbs")
    return os.path.join(thumbs_dir, filename)

def ensure_compressed(image_path: str, quality: int = 85, max_size: tuple = (1920, 1920)) -> str:
    """
    確保圖片有壓縮版本可用。如果沒有壓縮版本，則立即進行壓縮。
    返回可使用的圖片路徑（壓縮版本或原圖）
    """
    try:
        thumbs_path = get_thumbs_path(image_path)
        
        # 如果壓縮版本已存在，直接返回
        if os.path.exists(thumbs_path):
            return thumbs_path

        # 確保 thumbs 資料夾存在
        thumbs_dir = os.path.dirname(thumbs_path)
        os.makedirs(thumbs_dir, exist_ok=True)

        # 進行圖片壓縮
        with Image.open(image_path) as img:
            # 轉換為 RGB 模式（處理 RGBA 圖片）
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            # 調整圖片大小（如果需要）
            if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # 保存壓縮後的圖片
            img.save(thumbs_path, 'JPEG', quality=quality, optimize=True)
            print(f"已壓縮: {os.path.basename(image_path)}")
            return thumbs_path
            
    except Exception as e:
        print(f"壓縮圖片失敗 {os.path.basename(image_path)}: {e}")
        return image_path  # 如果壓縮失敗，返回原圖路徑

def get_image_url(image_dir: str, filename: str, use_compressed: bool = True) -> str:
    """
    獲取圖片URL。如果指定使用壓縮版本，會按需進行壓縮。
    """
    abs_path = os.path.join(CANDIDATES_ROOT, image_dir, filename)
    
    if use_compressed:
        # 確保有壓縮版本可用
        actual_path = ensure_compressed(abs_path)
        rel_path = os.path.relpath(actual_path, CANDIDATES_ROOT)
    else:
        # 使用原圖
        rel_path = os.path.join(image_dir, filename)
    
    encoded_path = quote(rel_path.replace("\\", "/"))
    return f"/candidate_images/{encoded_path}"

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

def get_admin_product_image_info_list(image_dir: str) -> List[dict]:
    """
    回傳 image_info list：[{
        "url": "/candidate_images/xxx/thumbs/xxx.jpg",  # 優先使用壓縮版本
        "filename": "xxx.jpg"                          # 保持原始檔名
    }]
    為了讓前端可以顯示與篩選。當圖片實際顯示時才會觸發壓縮。
    """
    filenames = _get_sorted_images(image_dir)
    result = []
    
    for filename in filenames:
        # 使用 get_image_url 來獲取圖片 URL（壓縮會在實際訪問時進行）
        url = get_image_url(image_dir, filename)
        result.append({
            "filename": filename,
            "url": url
        })
    return result

def get_main_image_url(image_dir: str) -> Optional[str]:
    """
    回傳第一張圖片的網址
    """
    files = _get_sorted_images(image_dir)
    if not files:
        return None

    # 使用第一張圖片，並確保它有壓縮版本
    return get_image_url(image_dir, files[0])

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

def get_images_url(image_dir: str, limit: int = 9) -> List[str]:
    """
    返回指定資料夾中的前 N 張圖片的 URL，用於 Excel 匯出
    預設最多返回 9 張（Shopee 限制）
    如果使用 USE_IMAGE_URL=true，則返回完整的 URL；否則返回本地路徑
    """
    files = _get_sorted_images(image_dir)[:limit]
    use_url = os.getenv("USE_IMAGE_URL", "false").lower() == "true"
    base_url = os.getenv("IMAGE_URL_BASE", "")
    
    if not files:
        return []
    
    result = []
    for filename in files:
        abs_path = os.path.join(CANDIDATES_ROOT, image_dir, filename)
        
        # 獲取實際使用的圖片路徑（按需壓縮）
        actual_path = ensure_compressed(abs_path) if use_url else abs_path
        rel_path = os.path.relpath(actual_path, CANDIDATES_ROOT)
        rel_path = rel_path.replace("\\", "/")
        
        if use_url:
            # 返回完整的 URL（用於 Shopee 上傳）
            result.append(f"https://{base_url}/candidate_images/{quote(rel_path)}")
        else:
            # 返回本地路徑
            result.append(actual_path)
    
    return result

