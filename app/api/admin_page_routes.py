# 📁 app/api/admin_page_routes.py
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.utils.template_engine import templates
from app.constants.status_labels import STATUS_LABELS

admin_page_router = APIRouter(prefix="/admin", tags=["admin_pages"])

@admin_page_router.get("/candidates", response_class=HTMLResponse)
def show_candidates_page(request: Request):
    return templates.TemplateResponse("admin/candidates_page.html", {
        "request": request,
        "candidate_images_prefix": "/candidate_images/",
        "status_labels": STATUS_LABELS
    })

@admin_page_router.get("/products", response_class=HTMLResponse)
def show_products_page(request: Request):
    return templates.TemplateResponse("admin/products_page.html", {
        "request": request,
        "candidate_images_prefix": "/candidate_images/",
        "status_labels": STATUS_LABELS
    })
