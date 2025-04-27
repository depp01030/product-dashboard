import os
import shutil
from datetime import datetime
from typing import List

from fastapi import UploadFile, HTTPException

from app.utils.config import PRODUCTS_ROOT  
from app.utils.path_tools import get_abs_folder_path


# app/utils/r2_uploader.py

import os
from pathlib import Path
import boto3
from botocore.exceptions import ClientError
from typing import Union, BinaryIO
from dotenv import load_dotenv

# ⏬ 載入環境變數（建議你放在 .env）
load_dotenv()

# === Cloudflare R2 設定 ===
R2_BUCKET = os.getenv("R2_BUCKET", "shopee-images")
R2_ENDPOINT = os.getenv("R2_ENDPOINT")
R2_ACCOUNT_ID = os.getenv("R2_ACCOUNT_ID")
ACCESS_KEY = os.getenv("R2_ACCESS_KEY")
SECRET_KEY = os.getenv("R2_SECRET_KEY")
print(R2_ENDPOINT)
print(R2_ACCOUNT_ID)
print(ACCESS_KEY)
print(SECRET_KEY)
# === 初始化 boto3 client ===
session = boto3.session.Session()
r2_client = session.client(
    service_name="s3",
    endpoint_url=R2_ENDPOINT,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
)

def upload_file_to_r2(
    file_obj: Union[Path, BinaryIO],
    key: str,
    content_type: str = "image/jpeg"
) -> str:
    """
    將檔案上傳到 R2，回傳公開圖片網址
    :param file_obj: 檔案路徑（Path）或檔案物件（UploadFile.file）
    :param key: 在 bucket 中的路徑（如：A001/001_商品名/1.jpg）
    :param content_type: 檔案類型（預設為 image/jpeg）
    """ 

    try:
        if isinstance(file_obj, Path): 
            r2_client.upload_file(
                Filename=str(file_obj),
                Bucket=R2_BUCKET,
                Key=key,
                ExtraArgs={"ACL": "public-read", "ContentType": content_type},
            )
        else:
            r2_client.upload_fileobj(
                Fileobj=file_obj,
                Bucket=R2_BUCKET,
                Key=key,
                ExtraArgs={"ACL": "public-read", "ContentType": content_type},
            )

        # 成功後回傳公開網址 
        return f"{R2_ENDPOINT}/{R2_BUCKET}/{key}"

    except BaseException as e:
        print(f"❌ 上傳失敗：{e}")
        raise
