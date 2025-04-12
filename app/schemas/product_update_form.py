from typing import Optional, List
from fastapi import Form

class ProductUpdateForm:
    def __init__(
        self,
        name: str = Form(...),
        description: str = Form(None),
        price: float = Form(None),
        stall_name: Optional[str] = Form(None),
        item_status: Optional[str] = Form(None),
        material: Optional[str] = Form(None),
        size_note: Optional[str] = Form(None),
        real_stock: Optional[int] = Form(None),
        custom_type: Optional[str] = Form(None),
        colors: Optional[str] = Form(""),
        sizes: Optional[str] = Form(""),
        selected_images: Optional[str] = Form(""),
        main_image: Optional[str] = Form(None)
    ):
        self.name = name
        self.description = description
        self.price = price
        self.stall_name = stall_name
        self.item_status = item_status
        self.material = material
        self.size_note = size_note
        self.real_stock = real_stock
        self.custom_type = custom_type
        self.colors = [c.strip() for c in colors.split(",") if c.strip()]
        self.sizes = [s.strip() for s in sizes.split(",") if s.strip()]
        self.selected_images = [i.strip() for i in selected_images.split(",") if i.strip()]
        self.main_image = main_image
