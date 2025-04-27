# 📁 app/api/admin_data_routes.py
from fastapi import APIRouter, Request, Depends, Form, Query, File, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta

from app.utils.db import get_db
from app.utils.template_engine import templates
from app.constants.status_labels import STATUS_LABELS
 
from app.models.product import Product
from app.schemas.product import ProductInDB, ProductUpdate, ProductCreate, ProductQuery
from app.schemas.product_update_form import ProductUpdateForm 
from app.services.product_service import (
    create_product,
    update_product,
    delete_product,
    query_products_with_filters
)
from app.services.import_service import import_candidates_from_folder
from app.utils.image_tools import get_admin_product_image_info_list

admin = APIRouter(prefix="/admin", tags=["admin_data"])

