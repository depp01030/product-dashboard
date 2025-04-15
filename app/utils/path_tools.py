import os 
from app.utils.config import load_env 
load_env()
PRODUCTS_ROOT = os.getenv("PRODUCTS_ROOT", "")


def _get_item_folder(stall_name, product_name):
    '''
    stall_name : 攤位名稱
    product_name : 商品名稱
    '''
    # 1. 先將攤位名稱和商品名稱進行處理，去除特殊字元
    if stall_name is None or stall_name == "":
        stall_name = "tmp_stall"
    if product_name is None or product_name == "":
        raise ValueError("商品名稱不能為空")  
    # 2. 將攤位名稱和商品名稱組合成資料夾名稱
    folder_path = os.path.join(stall_name, product_name)
    return folder_path
def _ensure_folder_exist(folder_path: str):
    '''
    folder_path : 資料夾路徑 relative path
    '''
    abs_folder_path = get_abs_folder_path(folder_path)
    if os.path.exists(abs_folder_path):
        return True
    os.makedirs(abs_folder_path, exist_ok=True)
    return False
def init_item_folder(stall_name, product_name):
    """
    自動生成 item_folder 名稱並確保對應資料夾存在於 PRODUCTS_ROOT 下。
    回傳的是相對於 PRODUCTS_ROOT 的 folder_path（即 item_folder 名稱）
    """
    item_folder = _get_item_folder(stall_name, product_name)
    _ensure_folder_exist(item_folder)
    return item_folder
def get_abs_folder_path(folder_path: str) -> str:
    """
    將 item_folder（相對於 PRODUCTS_ROOT）轉為絕對路徑。
    適合用於實際存取資料夾、圖片操作等情境。
    """
    return os.path.join(PRODUCTS_ROOT, folder_path)







