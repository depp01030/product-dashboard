# 📁 app/api/admin/product_images.py

from fastapi import APIRouter, UploadFile, Form, Request, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated, Optional, List

from app.schemas.product_image import (
    ProductImageSubmission,
    ProcessedImageInfo,
    ProductImageBase,
)
from app.utils.db import get_db
from app.services import product_image_service
from app.services.image_service.base_image_service import get_image_service, BaseImageService

router = APIRouter(prefix="/api/admin/product-image", tags=["ProductImages"])


# ------------------------------------------------------
# 💾 A1 - 儲存圖片編輯變更（新增 / 更新 / 刪除）
# POST /product-image/process
# ------------------------------------------------------
@router.post("/process", response_model=dict)
async def save_image_changes(
    product_id: Annotated[int, Form(...)],
    images: Annotated[str, Form(...)],
    request: Request,
    db: Session = Depends(get_db),
    image_service: BaseImageService = Depends(get_image_service),
):
    form = await request.form()
    files = {k: v for k, v in form.items() if isinstance(v, UploadFile)}
 
    result = await product_image_service.process_product_images(
        db=db,
        product_id=product_id,
        image_data_json=images,
        files=files,
        image_service=image_service,
    )
    return result


# ------------------------------------------------------
# 📦 A2 - 取得某商品的所有圖片資訊
# GET /product-image/product/{product_id}
# ------------------------------------------------------
@router.get("/product/{product_id}", response_model=List[ProcessedImageInfo])
def get_product_images(
    product_id: int,
    db: Session = Depends(get_db),
    image_service: BaseImageService = Depends(get_image_service),
):
    return product_image_service.get_images_info_by_product_id(
        db=db,
        product_id=product_id,
        image_service=image_service,
    )


# ------------------------------------------------------
# 🖼️ A3 - 單張圖片上傳（預覽用）
# POST /product-image/upload
# ------------------------------------------------------
@router.post("/upload", response_model=ProcessedImageInfo)
async def upload_single_image(
    product_id: Annotated[int, Form(...)],
    file: Annotated[UploadFile, Form(...)],
    db: Session = Depends(get_db),
    image_service: BaseImageService = Depends(get_image_service),
):
    return await product_image_service.upload_single_image(
        db=db,
        product_id=product_id,
        file=file,
        image_service=image_service,
    )


# ------------------------------------------------------
# 🔍 A4 - 根據圖片 ID 查詢圖片
# GET /product-image/{image_id}
# ------------------------------------------------------
@router.get("/{image_id}", response_model=ProcessedImageInfo)
def get_image_by_id(
    image_id: int,
    db: Session = Depends(get_db),
    image_service: BaseImageService = Depends(get_image_service),
): 
    return product_image_service.get_image_by_id(
        db=db,
        image_id=image_id,
        image_service=image_service,
    )


# ------------------------------------------------------
# ➕ A5 - 新增圖片 metadata (僅新增metadata)
# POST /product-image/
# ------------------------------------------------------
@router.post("/", response_model=ProcessedImageInfo, status_code=status.HTTP_201_CREATED)
def create_image_metadata(
    data: ProductImageBase,
    db: Session = Depends(get_db),
):
    return product_image_service.create_image_metadata(db, data)


# ------------------------------------------------------
# ✏️ A6 - 更新圖片 metadata (僅更新metadata)
# PATCH /product-image/{image_id}
# ------------------------------------------------------
@router.patch("/{image_id}", response_model=ProcessedImageInfo)
def update_image_metadata(
    image_id: int,
    patch: ProductImageBase,
    db: Session = Depends(get_db),
):
    return product_image_service.update_image_metadata(db, image_id, patch)
