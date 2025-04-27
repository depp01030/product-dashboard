// 📁 static/js/pages/products-page.js
import { initProductPage } from "../utils/init-product-page.js";

initProductPage({
  containerId: "product-list",
  filterFormId: "filter-form",
  searchBtnId: "search-btn",
  addItemBtnId: "add-item-btn",
  loadMoreBtnId: "load-more-btn",
  showFields: [
    "source_url",
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

// 👇 這裡加
const container = document.getElementById("product-list");
if (container) {
  const img = document.createElement("img");
  img.src = "https://pub-bb9127b0307b40cc94deb60de4f6422f.r2.dev/test_uploads/QrCode.jpg";
  img.alt = "測試圖片";
  img.style.width = "200px";
  img.style.marginBottom = "1rem";
  container.prepend(img);
}