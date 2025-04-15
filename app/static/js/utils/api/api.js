// 📁 static/js/utils/api.js

/**
 * 發送查詢請求，根據條件取得商品列表
 *
 * @param {Object} filters - 篩選條件
 * @param {number} offset - 分頁起點
 * @param {number} limit - 每頁筆數
 * @returns {Promise<Array>} - 商品資料陣列
 */
export async function fetchProductsWithFilters(filters = {}, offset = 0, limit = 20) {
    const url = new URL("/admin/api/products", window.location.origin);
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== "") {
        url.searchParams.append(key, value);
      }
    });
    url.searchParams.append("offset", offset);
    url.searchParams.append("limit", limit);
  
    const res = await fetch(url);
    if (!res.ok) {
      console.error("查詢商品失敗", res);
      return [];
    }
  
    return await res.json();
  }
  