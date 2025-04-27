# app/schemas/pagination.py

from typing import List, Generic, TypeVar
from pydantic import BaseModel
from pydantic.generics import GenericModel
from app.schemas.product import ProductInDB
T = TypeVar("T")

class PaginatedResponse(GenericModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int

class PaginatedProducts(PaginatedResponse[ProductInDB]):
    """商品清單回傳"""