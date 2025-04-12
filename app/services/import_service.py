# app/services/import_service.py

import os
from app.utils.db import SessionLocal
from app.models.product import Product
from app.models.enums import ItemStatusEnum
from app.utils.config import load_env

load_env()
CANDIDATES_ROOT = os.getenv("CANDIDATES_ROOT")

def import_candidates_from_folder() -> int:
    db = SessionLocal()
    inserted = 0

    for stall_name in os.listdir(CANDIDATES_ROOT):
        stall_path = os.path.join(CANDIDATES_ROOT, stall_name)
        if not os.path.isdir(stall_path):
            continue

        for folder in os.listdir(stall_path):
            folder_path = os.path.join(stall_path, folder)
            if not os.path.isdir(folder_path):
                continue

            image_dir = f"{stall_name}/{folder}"
            existing = db.query(Product).filter_by(image_dir=image_dir).first()
            if existing:
                continue

            product = Product(
                name=folder,
                stall_name=stall_name,
                image_dir=image_dir,
                item_status=ItemStatusEnum.candidate
            )
            db.add(product)
            inserted += 1

    db.commit()
    db.close()
    return inserted
