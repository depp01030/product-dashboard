// static/js/products_page.js

import { fetchProductsWithFilters } from "./api.js";
import {
  clearProductList,
  appendProductCard,
  updateProductCount,
} from "./dom.js";

let currentOffset = 0;
const PAGE_SIZE = 20;
let isLoading = false;

const loadMoreBtn = document.getElementById("load-more-btn");  // ✅ 修正這個 id
const searchBtn = document.getElementById("search-btn");

searchBtn.addEventListener("click", () => {
  currentOffset = 0;
  clearProductList();
  loadNextPage(true);
});

loadMoreBtn.addEventListener("click", () => {
  loadNextPage(false);
});

async function loadNextPage(isNewSearch = false) {
  if (isLoading) return;
  isLoading = true;

  const query = getQueryParams();
  const offset = isNewSearch ? 0 : currentOffset;
  query.offset = offset;
  query.limit = PAGE_SIZE;

  console.log("🔍 發送查詢：", query);  // ✅ 加這行 debug 看 URL

  try {
    const products = await fetchProductsWithFilters(query);
    if (isNewSearch) clearProductList();
    products.forEach((p) => appendProductCard(p));
    updateProductCount(offset + products.length);

    currentOffset += products.length;
    loadMoreBtn.style.display = products.length < PAGE_SIZE ? "none" : "inline-block";
  } catch (err) {
    console.error("載入失敗", err);
  }

  isLoading = false;
}

function getQueryParams() {
  return {
    from_date: document.getElementById("filter-from-date").value,
    stall: document.getElementById("filter-stall").value,
    status: document.getElementById("filter-status").value,
    name: document.getElementById("filter-name").value,
  };
}
console.log("🔍 初始化載入商品列表...");
loadNextPage(true);
