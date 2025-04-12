// static/js/dom.js
import { generateItemStatusOptions } from "./item_status_options.js";
/**
 * ✅ DOM 操作模組
 * ------------------------
 * 此模組負責所有與「頁面渲染」相關的操作，
 * 包括：
 * - 動態建立商品卡片
 * - 插入商品清單至畫面
 * - 清空現有畫面內容
 * - 顯示符合條件的商品總數
 *
 * 注意：這裡不負責 API 呼叫、不負責查詢條件邏輯，
 * 只處理「資料拿到之後，如何渲染到畫面上」的部分。
 */

const productListEl = document.getElementById("product-list");
const productCountEl = document.getElementById("product-count");

/**
 * ✅ 清空現有商品列表
 */
export function clearProductList() {
    productListEl.innerHTML = "";
}

/**
 * ✅ 更新商品總數顯示
 */
export function updateProductCount(count) {
    productCountEl.textContent = count;
}

/**
 * ✅ 將商品插入到 DOM
 */
export function appendProductCard(product) {
    const card = renderProductCard(product);
    productListEl.appendChild(card);
}

/**
 * ✅ 產生單一商品的卡片 HTML
 */
export function renderProductCard(product) {
    const card = document.createElement("form");
    card.method = "post";
    card.action = `/admin/products/${product.id}/update`;
    card.className = "card mb-4 p-3 shadow-sm";
  
    const imagePrefix = `/candidate_images/${encodeURIComponent(product.image_dir)}/`;
    const previewImages = Array.isArray(product.image_list) ? product.image_list.slice(0, 3) : [];
    const allImages = Array.isArray(product.image_list) ? product.image_list : [];
  
    card.innerHTML = `
      <!-- 🔢 ID + 檔口名稱 + 儲存 -->
      <div class="mb-3 d-flex justify-content-between align-items-center">
        <div>
          <strong>#${product.id}</strong>
          <label class="form-label ms-2 mb-0">檔口：</label>
          <input name="stall_name" class="form-control d-inline-block w-auto" value="${product.stall_name || ""}">
        </div>
        <button type="submit" class="btn btn-success btn-sm">儲存</button>
      </div>
  
      <div class="row">
        <!-- 左側：圖片預覽 -->
        <div class="col-md-5">
          <div class="d-flex gap-2 mb-2">
            ${previewImages.map(img => `
              <img src="${imagePrefix}${encodeURIComponent(img.filename)}"
                   loading="lazy"
                   class="img-thumbnail"
                   style="max-height: 200px;">`
            ).join("")}
          </div>
  
          <!-- 🔽 展開收合按鈕 -->
          <button class="btn btn-outline-secondary btn-sm mb-2" type="button"
                  data-bs-toggle="collapse" data-bs-target="#collapse-${product.id}">
            顯示全部圖片
          </button>
  
          <!-- 📦 所有圖片勾選區 -->
          <div class="collapse" id="collapse-${product.id}">
            <div class="d-flex flex-wrap gap-2 mt-2">
              ${allImages.map(img => `
                <div class="border rounded p-2 text-center" style="width: 100px;">
                  <img src="${imagePrefix}${encodeURIComponent(img.filename)}"
                       loading="lazy" class="img-fluid mb-1" style="max-height: 80px;">
                  <div>
                    <input type="checkbox" name="selected_images" value="${img.filename}"
                           ${product.selected_images?.includes(img.filename) ? "checked" : ""}>
                    使用
                  </div>
                  <div>
                    <input type="radio" name="main_image" value="${img.filename}"
                           ${product.main_image === img.filename ? "checked" : ""}>
                    主圖
                  </div>
                </div>`
              ).join("")}
            </div>
          </div>
        </div>
  
        <!-- 右側：基本欄位 -->
        <div class="col-md-7">
          <div class="mb-2">
            <label class="form-label">商品名稱</label>
            <input name="name" class="form-control" value="${product.name || ""}">
          </div>
          <div class="mb-2">
            <label class="form-label">商品描述</label>
            <textarea name="description" class="form-control" rows="2">${product.description || ""}</textarea>
          </div>
          <div class="row mb-2">
            <div class="col-md-6">
              <label class="form-label">價格</label>
              <input name="price" type="number" class="form-control" value="${product.price || ""}">
            </div>
            <div class="col-md-6">
              <label class="form-label">庫存</label>
              <input name="stock" type="number" class="form-control" value="${product.stock || ""}">
            </div>
          </div>
          <div class="mb-2">
            <label class="form-label">狀態</label>
                <select name="item_status" class="form-select">
                ${generateItemStatusOptions(product.item_status)}
                </select>
          </div>
        </div>
      </div>
    `;
  
    return card;
  }
  