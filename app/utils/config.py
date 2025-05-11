import os
from dotenv import load_dotenv

# ✅ 自動讀取 .env
load_dotenv(dotenv_path=".env", override=True)

IMAGE_STORAGE_BACKEND = os.getenv("IMAGE_STORAGE_BACKEND") 
# ───────────── 資料庫 ─────────────
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "shopee_db")

DATABASE_URL = (
    f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# ───────────── 資料夾 ─────────────
IS_DOCKER = os.getenv("IS_DOCKER", "false") == "true"
PRODUCTS_ROOT = (
    os.getenv("DOCKER_PRODUCTS_ROOT")
    if IS_DOCKER
    else os.getenv("PRODUCTS_ROOT")
)

# ───────────── 圖片儲存 ─────────────
IMAGE_LOCAL_BASE_DIR = PRODUCTS_ROOT
IMAGE_ROUTE_PREFIX = os.getenv("IMAGE_LOCAL_BASE_URL", "/images")

# ───────────── 圖床網址 ─────────────
if IMAGE_STORAGE_BACKEND == "r2":
    R2_BUCKET = os.getenv("R2_BUCKET")
    R2_ENDPOINT = os.getenv("R2_ENDPOINT")
    R2_ACCESS_KEY = os.getenv("R2_ACCESS_KEY")
    R2_TOKEN = os.getenv("R2_TOKEN")
    R2_SECRET_KEY = os.getenv("R2_SECRET_KEY")
    R2_IMAGE_URL_BASE = os.getenv("R2_IMAGE_URL_BASE") 
    if not R2_IMAGE_URL_BASE:
        raise ValueError("R2_IMAGE_URL_BASE must be set when using R2 storage.")
    IMAGE_URL_BASE = R2_IMAGE_URL_BASE  # R2 的網址

elif IMAGE_STORAGE_BACKEND == "local":
    APP_BASE_URL = os.getenv("APP_BASE_URL", "http://localhost:8000")
    IMAGE_URL_BASE = f"{APP_BASE_URL.rstrip('/')}{IMAGE_ROUTE_PREFIX}"
else:
    raise ValueError(f"Unsupported image storage backend: {IMAGE_STORAGE_BACKEND}")
print(f"[config] IMAGE_URL_BASE: {IMAGE_URL_BASE}")
