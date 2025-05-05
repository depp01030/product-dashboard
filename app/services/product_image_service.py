# 📁 app/services/product_image_service.py

from typing import List, Dict
from fastapi import UploadFile
from sqlalchemy.orm import Session
from uuid import uuid4
from app.models import ProductImage, Product
from app.services.image_service.base_image_service import BaseImageService
from app.schemas.product_image import (
    ProductImageSubmission,
    ProcessedImageInfo,
    ProductImageBase,
)
from app.services.image_service.base_image_service import get_image_service
# ------------------------------------------------------
# 💾 A1 - 儲存圖片編輯變更（新增 / 更新 / 刪除）
# ------------------------------------------------------
async def process_product_images(
    db: Session,
    product_id: int,
    image_data_json: str,
    files: Dict[str, UploadFile],
    image_service: BaseImageService,
) -> dict:
    import json
    from app.models import ProductImage, Product
    print(image_data_json)
    submissions = json.loads(image_data_json)
    results = []
    message = {}
    error = {}

    # ✅ 提前查出商品（只查一次）
    product = db.query(Product).get(product_id)
    if not product:
        raise ValueError("Product not found")

    for data in submissions:
        action = data.get("action")
        temp_id = data.get("temp_id")
        image_id = data.get("id")
        is_main = data.get("is_main", False)
        is_selected = data.get("is_selected", False)

        try:
            if action == "new":
                file_key = f"file_{temp_id}"
                file = files.get(file_key)
                if not file:
                    error[temp_id] = "缺少對應圖片檔案"
                    continue

                file_name = file.file_name
                local_path = await image_service.save_file(file, product, file_name)

                image = ProductImage(
                    product_id=product_id,
                    file_name=file_name,
                    is_main=is_main,
                    is_selected=is_selected, 
                )
                db.add(image)
                db.commit()
                db.refresh(image)

            elif action == "update":
                image = db.query(ProductImage).get(image_id)
                if not image:
                    error[image_id] = "找不到圖片"
                    continue
                print('hi')
                image.is_main = is_main
                image.is_selected = is_selected
                db.commit()
                db.refresh(image)

            elif action == "delete":
                image = db.query(ProductImage).get(image_id)
                if not image:
                    error[image_id] = "找不到圖片"
                    continue
                # await image_service.delete_file(image.local_path)
                db.delete(image)
                db.commit()
                continue  # 不回傳已刪除項目

            else:
                error[temp_id or image_id] = f"未知動作：{action}"
                continue

            # ✅ 成功的圖片組回傳物件 
            image_info = ProcessedImageInfo.model_validate(image, from_attributes=True)
            image_info.url = image_service.get_image_url(product, image.file_name)
            results.append(image_info)

        except Exception as e:
            error[temp_id or image_id] = str(e)

    return {
        "images": results,
        "message": message,
        "error": error,
    }


# ------------------------------------------------------
# 📦 A2 - 取得某商品的所有圖片資訊
# ------------------------------------------------------
def get_images_info_by_product_id(
    db: Session,
    product_id: int,
    image_service: BaseImageService,
) -> List[ProcessedImageInfo]:
    images = db.query(ProductImage).filter(ProductImage.product_id == product_id).all()
    product = db.query(Product).get(product_id)
    if not product:
        raise ValueError("Product not found")

    result = []
    for img in images:
        image_info = ProcessedImageInfo.model_validate(img, from_attributes=True)
        image_info.url = image_service.get_image_url(product, img.file_name)
        result.append(image_info)

    return result


# ------------------------------------------------------
# 🖼️ A3 - 單張圖片上傳（預覽用）
# ------------------------------------------------------
async def upload_single_image(
    db: Session,
    product_id: int,
    file: UploadFile,
    image_service: BaseImageService,
) -> ProcessedImageInfo:
    product = db.query(Product).get(product_id)
    if not product:
        raise ValueError("Product not found")

    temp_id = uuid4().hex
    local_path = await image_service.save_file(product_id, file, temp_id)
    file_name = file.file_name or f"{temp_id}.jpg"

    image = ProductImage(
        product_id=product_id,
        file_name=file_name, 
        is_main=False,
        is_selected=True,
    )
    db.add(image)
    db.commit()
    db.refresh(image)

    image_info = ProcessedImageInfo.model_validate(image, from_attributes=True)
    image_info.url = image_service.get_image_url(product, file_name)
    return image_info


# ------------------------------------------------------
# 🔍 A4 - 根據圖片 ID 查詢圖片資訊
# ------------------------------------------------------
def get_image_by_id(
    db: Session,
    image_id: int,
    image_service: BaseImageService,
) -> ProcessedImageInfo:
    image = db.query(ProductImage).get(image_id)
    if not image:
        raise ValueError("Image not found")

    product = db.query(Product).get(image.product_id)
    if not product:
        raise ValueError("Product not found")

    image_info = ProcessedImageInfo.model_validate(image, from_attributes=True)
    image_info.url = image_service.get_image_url(product, image.file_name)
    return image_info


# ------------------------------------------------------
# ➕ A5 - 新增圖片 metadata
# ------------------------------------------------------
def create_image_metadata(
    db: Session,
    data: ProductImageBase,
) -> ProcessedImageInfo:
    image = ProductImage(**data.model_dump())
    db.add(image)
    db.commit()
    db.refresh(image)

    product = db.query(Product).get(image.product_id)
    image_info = ProcessedImageInfo.model_validate(image, from_attributes=True)
    return image_info


# ------------------------------------------------------
# ✏️ A6 - 更新圖片 metadata
# ------------------------------------------------------
def update_image_metadata(
    db: Session,
    image_id: int,
    patch: ProductImageBase,
) -> ProcessedImageInfo:
    image_service = get_image_service()
    image = db.query(ProductImage).get(image_id)
    if not image:
        raise ValueError("Image not found")

    for field, value in patch.model_dump(exclude_unset=True).items():
        setattr(image, field, value)
    db.commit()
    db.refresh(image)

    product = db.query(Product).get(image.product_id)
    image_info = ProcessedImageInfo.model_validate(image, from_attributes=True)
    image_info.url = image_service.get_image_url(product, image.file_name)
    return image_info
