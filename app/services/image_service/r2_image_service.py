import boto3
from fastapi import UploadFile
from urllib.parse import quote_plus
from app.models.product import Product
from app.utils.config import (
    R2_BUCKET, R2_ENDPOINT, R2_ACCESS_KEY, R2_SECRET_KEY, R2_IMAGE_URL_BASE
)

# 初始化 R2 S3 client
s3_client = boto3.client(
    "s3",
    endpoint_url=R2_ENDPOINT,
    region_name="auto",  # ✅ 指定 region 為 auto
    aws_access_key_id=R2_ACCESS_KEY,
    aws_secret_access_key=R2_SECRET_KEY,
)

class R2ImageService:
    def _get_object_key(self, product: Product, file_name: str) -> str:
        return f"{product.stall_name}/{product.name}/{file_name}"

    async def save_file(self, file: UploadFile, product: Product, file_name: str) -> str:
        key = self._get_object_key(product, file_name)
        content = await file.read()
        s3_client.put_object(
            Bucket=R2_BUCKET,
            Key=key,
            Body=content,
            ContentType=file.content_type,
        )
        return key

    def delete_file(self, product: Product, file_name: str) -> bool:
        key = self._get_object_key(product, file_name)
        try:
            s3_client.delete_object(Bucket=R2_BUCKET, Key=key)
            return True
        except Exception as e:
            print("[R2 delete error]", e)
            return False

    def get_image_url(self, product: Product, file_name: str) -> str:
        return self._get_signed_url(product, file_name, expires_in=600)

    def _get_signed_url(self, product: Product, file_name: str, expires_in: int = 600) -> str:
        key = self._get_object_key(product, file_name)
        url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": R2_BUCKET, "Key": key},
            ExpiresIn=expires_in,
        ) 
        return url

