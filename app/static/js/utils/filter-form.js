// 📁 static/js/utils/filter-form.js

/**
 * 從篩選表單中讀取欄位值，轉為 filters 物件
 * @param {HTMLFormElement} form 
 * @returns {Object} filters
 */
export function getFiltersFromForm(form) {
    if (!form) return {};
    const formData = new FormData(form);
    const filters = {};
    for (const [key, value] of formData.entries()) {
      filters[key] = value.trim();
    }
    return filters;
  }
  
  /**
   * 可選功能：綁定篩選欄位的 enter 觸發事件
   */
  export function bindFilterEvents(form, onSearch) {
    if (!form || !onSearch) return;
    form.addEventListener("submit", e => {
      e.preventDefault();
      onSearch();
    });
  }
  