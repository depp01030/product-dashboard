import os
from dotenv import load_dotenv

# ✅ 先載入 .env
load_dotenv()

# ────────────────────────────────────────────────
# 📦 1. 資料庫設定區
# ────────────────────────────────────────────────
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "shopee_db")

DATABASE_URL = (
    f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# ────────────────────────────────────────────────
# 🗂 2. 資料夾路徑設定
# ────────────────────────────────────────────────
CANDIDATES_ROOT = os.getenv("CANDIDATES_ROOT", "./Candidates_root")
PRODUCTS_ROOT = os.getenv("PRODUCTS_ROOT", "./products_root")

# ────────────────────────────────────────────────
# 🖼 3. 圖片儲存設定
# ────────────────────────────────────────────────
IMAGE_STORAGE_BACKEND = os.getenv("IMAGE_STORAGE_BACKEND", "local")
IMAGE_LOCAL_BASE_DIR = os.getenv("IMAGE_LOCAL_BASE_DIR", PRODUCTS_ROOT)
IMAGE_LOCAL_BASE_URL = os.getenv("IMAGE_LOCAL_BASE_URL", "/images")

# ────────────────────────────────────────────────
# 🌐 4. 應用程式設定
# ────────────────────────────────────────────────
APP_BASE_URL = os.getenv("APP_BASE_URL", "http://localhost:8000")
IMAGE_URL_BASE = f"{APP_BASE_URL.rstrip('/')}{IMAGE_LOCAL_BASE_URL}"

# ✅ Debug 用印出圖片網址 base
print(f"IMAGE_URL_BASE: {IMAGE_URL_BASE}")
