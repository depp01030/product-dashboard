// 📁 static/js/pages/products-page.js
import { initProductPage } from "../utils/init-product-page.js";

initProductPage({
  containerId: "product-list",
  filterFormId: "filter-form",
  searchBtnId: "search-btn",
  addItemBtnId: "add-item-btn",
  loadMoreBtnId: "load-more-btn",
  showFields: [
    "stall_name",
    "source",
    "name",
    "description",
    "custom_type",
    "material",
    "price",
    "colors",
    "sizes",
    "item_status"
  ],
  submitPath: "/admin/products",
  defaultFilters: { item_status: "product" }
});
