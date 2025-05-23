from typing import Optional, List
from fastapi import Form

class ProductUpdateForm:
    def __init__(
        self,
        name: str = Form(None),
        description: str = Form(None),

        purchase_price: float = Form(None),
        total_cost: float = Form(None),
        price: float = Form(None),
        
        stall_name: Optional[str] = Form(None),
        source: Optional[str] = Form(None),
        source_url: Optional[str] = Form(None),
        item_status: Optional[str] = Form("product"),
        material: Optional[str] = Form(None),
        size_metrics: Optional[str] = Form("{}"),  # JSON string
        size_note: Optional[str] = Form(None),
        real_stock: Optional[int] = Form(None),
        custom_type: Optional[str] = Form(None),
        colors: Optional[str] = Form(""),
        sizes: Optional[str] = Form(""),
        item_folder: Optional[str] = Form(None),
        selected_images: Optional[List[str]] = Form(None),
        main_image: Optional[str] = Form(None)
    ):
        self.name = name
        self.description = description

        self.purchase_price = purchase_price
        self.total_cost = total_cost
        self.price = price
        
        self.stall_name = stall_name
        self.source = source
        self.source_url = source_url
        self.item_status = item_status
        self.material = material
        self.size_metrics = size_metrics  # Will be parsed as JSON in service
        self.size_note = size_note
        self.real_stock = real_stock
        self.custom_type = custom_type
        self.colors = [c.strip() for c in colors.split(",") if c.strip()]
        self.sizes = [s.strip() for s in sizes.split(",") if s.strip()] 
        
        self.item_folder = item_folder
        self.selected_images = selected_images or []
        self.main_image = main_image
