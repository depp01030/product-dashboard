// 📁 static/js/utils/render-card.js
import { renderImageModule } from "./render-image-module.js";

/**
 * 渲染商品卡片：
 * - 使用 row 佈局
 * - 左邊是商品資訊（欄位 + 按鈕）
 * - 右邊是圖片模組（展開 / 收合）
 */
export function renderProductCard(product, options = {}) {
  const {
    showFields = [],
    submitPath = "/admin/products",
    renderAsCheckbox = false
  } = options;

  const form = document.createElement("form");
  form.method = "post";
  form.action = `${submitPath}/${product.id}/update`;
  form.className = "card mb-4 p-3 shadow-sm w-100";

  const row = document.createElement("div");
  row.className = "row";

  // === 左側：商品欄位 ===
  const colLeft = document.createElement("div");
  colLeft.className = "col-md-7";
  colLeft.innerHTML = `
    <div class="mb-3 d-flex justify-content-between align-items-center">
      <div>
        <strong>#${product.id}</strong>
        ${showFields.includes("stall_name") ? `
          <label class="form-label ms-2 mb-0">檔口：</label>
          <input name="stall_name" class="form-control d-inline-block w-auto" value="${product.stall_name || ""}">
        ` : ""}
      </div>
      <button type="submit" class="btn btn-success btn-sm">儲存</button>
    </div>

    ${showFields.includes("name") ? `
      <div class="mb-2">
        <label class="form-label">商品名稱</label>
        <input name="name" class="form-control" value="${product.name || ""}">
      </div>
    ` : ""}
    ${showFields.includes("description") ? `
      <div class="mb-2">
        <label class="form-label">商品描述</label>
        <textarea name="description" class="form-control" rows="2">${product.description || ""}</textarea>
      </div>
    ` : ""}
    ${showFields.includes("price") ? `
      <div class="mb-2">
        <label class="form-label">價格</label>
        <input name="price" type="number" class="form-control" value="${product.price || ""}">
      </div>
    ` : ""}
    ${showFields.includes("stock") ? `
      <div class="mb-2">
        <label class="form-label">庫存</label>
        <input name="stock" type="number" class="form-control" value="${product.stock || ""}">
      </div>
    ` : ""}
    ${showFields.includes("item_status") ? (
      renderAsCheckbox ? `
        <div class="form-check">
          <input class="form-check-input" type="checkbox" name="item_status" id="check-status-${product.id}" value="product" ${product.item_status === "product" ? "checked" : ""}>
          <label class="form-check-label" for="check-status-${product.id}">
            標記為「已選」
          </label>
          <input type="hidden" name="item_status_unchecked" value="candidate">
        </div>
      ` : `
        <div class="mb-2">
          <label class="form-label">狀態</label>
          <select name="item_status" class="form-select">
            ${generateItemStatusOptions(product.item_status)}
          </select>
        </div>
      `)
    : ""}
  `;
  row.appendChild(colLeft);

  // === 右側：圖片模組 ===
  const colRight = document.createElement("div");
  colRight.className = "col-md-5";
  colRight.appendChild(renderImageModule(product));
  row.appendChild(colRight);

  form.appendChild(row);

  // 非跳轉式送出
  form.addEventListener("submit", async e => {
    e.preventDefault();
    const formData = new FormData(form);
    if (renderAsCheckbox && !formData.has("item_status")) {
      formData.set("item_status", "candidate");
    }
    const res = await fetch(form.action, {
      method: "POST",
      body: formData
    });
    const button = form.querySelector("button[type=submit]");
    if (res.ok) {
      button.innerHTML = `<span class="text-success">✅ 已儲存</span>`;
      button.disabled = true;
    } else {
      button.innerHTML = `<span class="text-danger">❌ 儲存失敗</span>`;
    }
    setTimeout(() => {
      button.innerHTML = "儲存";
      button.disabled = false;
    }, 1800);
  });

  return form;
}

function generateItemStatusOptions(current) {
  const values = ["candidate", "product", "ignore"];
  const labels = {
    candidate: "候選",
    product: "已選",
    ignore: "忽略"
  };
  return values.map(v => `<option value="${v}" ${v === current ? "selected" : ""}>${labels[v]}</option>`).join("");
}