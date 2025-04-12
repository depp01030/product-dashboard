// 📁 static/js/pages/products-page.js
import { initProductPage } from "../utils/init-product-page.js";

initProductPage({
  containerId: "product-list",
  filterFormId: "filter-form",
  searchBtnId: "search-btn",
  loadMoreBtnId: "load-more-btn",
  showFields: [
    "stall_name",
    "name",
    "description",
    "price",
    "stock",
    "item_status"
  ],
  submitPath: "/admin/products",
  defaultFilters: { item_status: "product" }
});
