// static/js/api.js

const API_BASE = "/admin/api/products";

/**
 * ✅ 發送 API 請求取得商品資料（篩選 + 分頁）
 * @param {Object} params - 篩選條件物件（from_date, stall, status, id, name）
 * @param {number} offset - 起始筆數（分頁）
 * @param {number} limit - 每頁筆數
 * @returns {Promise<Array>} 商品清單
 */
export async function fetchProductsWithFilters(params = {}, offset = 0, limit = 20) {
    const query = new URLSearchParams({ offset, limit });

    for (const key in params) {
        if (params[key]) {
            query.append(key, params[key]);
        }
    }

    const res = await fetch(`${API_BASE}/search?${query.toString()}`);
    if (!res.ok) {
        console.error("❌ 取得商品資料失敗", res.status);
        return [];
    }
    return await res.json();
}
