// 📁 static/js/pages/candidates-page.js
import { initProductPage } from "../utils/init-product-page.js";

initProductPage({
  containerId: "product-list",
  filterFormId: "filter-form",
  searchBtnId: "search-btn",
  loadMoreBtnId: "load-more-btn",
  showFields: ["stall_name", "name", "item_status"],
  submitPath: "/admin/products",
  defaultFilters: { item_status: "candidate" },
  renderAsCheckbox: true
});
