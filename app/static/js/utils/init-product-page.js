// 📁 static/js/utils/init-product-page.js

import { fetchProductsWithFilters } from "./api.js";
import { renderProductCard } from "./render-card.js";
import { clearList, appendToList, updateItemCount } from "./render-list.js";
import { getFiltersFromForm, bindFilterEvents } from "./filter-form.js";
import { resetPagination, getCurrentOffset, increaseOffset, shouldShowLoadMore, bindLoadMore } from "./pagination.js";

export function initProductPage(config) {
  const {
    containerId,
    filterFormId,
    searchBtnId,
    loadMoreBtnId,
    showFields,
    submitPath,
    defaultFilters = {},
    pageSize = 20,
    renderAsCheckbox = false
  } = config;

  const container = document.getElementById(containerId);
  const filterForm = document.getElementById(filterFormId);
  const searchBtn = document.getElementById(searchBtnId);
  const loadMoreBtn = document.getElementById(loadMoreBtnId);

  async function loadProducts({ reset = false } = {}) {
    if (reset) {
      resetPagination();
      clearList(container);
    }

    const filters = { ...defaultFilters, ...getFiltersFromForm(filterForm) };
    const offset = getCurrentOffset();
    const products = await fetchProductsWithFilters(filters, offset, pageSize);

    products.forEach(product => {
      const card = renderProductCard(product, {
        showFields,
        submitPath,
        renderAsCheckbox: config.renderAsCheckbox
      });
      appendToList(container, card);
    });

    updateItemCount();
    if (shouldShowLoadMore(products.length, pageSize)) {
      loadMoreBtn.style.display = "block";
    } else {
      loadMoreBtn.style.display = "none";
    }
    increaseOffset(products.length);
  }

  // 🔍 綁定查詢按鈕
  if (searchBtn) {
    searchBtn.addEventListener("click", () => loadProducts({ reset: true }));
  }

  // 🔁 載入更多
  if (loadMoreBtn) {
    bindLoadMore(loadMoreBtn, () => loadProducts());
  }

  // 初始載入
  loadProducts({ reset: true });
}
