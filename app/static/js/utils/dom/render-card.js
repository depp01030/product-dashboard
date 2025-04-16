// 📁 static/js/utils/dom/render-card.js
import { renderImageModule } from "./render-image-module.js";
import { initResizable } from "../resizable-layout.js";
import { submitProductForm } from "../form/form-submit.js";
import {
  SIZE_METRICS_BY_TYPE,
  SIZE_METRIC_LABELS,
  CUSTOM_TYPE_OPTIONS
} from "../data/metrics.js";
import {
  createDynamicListInput,
  createDynamicKVInput,
  extractDynamicListValues,
  extractDynamicKVValues
} from "./product-card-widget.js";

export function renderProductCard(product, options = {}) {
  const {
    showFields = [],
    submitPath = "/admin/products",
    renderAsCheckbox = false,
    onSubmit = submitProductForm
  } = options;

  if (!product.item_status) {
    product.item_status = "product";
  }

  const form = document.createElement("form");
  form.method = "post";
  form.action = `${submitPath}/${product.id}/update`;
  form.className = "card shadow border-0 mb-4 bg-white";

  const borderTop = document.createElement("div");
  borderTop.className = "border-top border-4 border-primary rounded-top";
  form.appendChild(borderTop);

  const cardBody = document.createElement("div");
  cardBody.className = "card-body p-4";
  cardBody.appendChild(renderHeader(product, showFields));

  const container = document.createElement("div");
  container.className = "resizable-container";

  const colLeft = document.createElement("div");
  colLeft.className = "resizable-left";
  colLeft.appendChild(renderLeftPanel(product, showFields));

  const splitter = document.createElement("div");
  splitter.className = "resizable-splitter";

  const colRight = document.createElement("div");
  colRight.className = "resizable-right";
  colRight.appendChild(renderImageModule(product));

  container.appendChild(colLeft);
  container.appendChild(splitter);
  container.appendChild(colRight);
  cardBody.appendChild(container);

  initResizable(container);
  form.appendChild(cardBody);

  form.addEventListener("submit", e => onSubmit(e, form, renderAsCheckbox));
  const deleteBtn = form.querySelector(".delete-btn");
  deleteBtn.addEventListener("click", async () => {
    if (!confirm(`確定要刪除 #${product.id} 嗎？`)) return;

    const res = await fetch(`/admin/products/${product.id}/delete`, {
      method: "DELETE"
    });

    if (res.ok) {
      form.closest(".col-12")?.remove();  // 把整張卡片從 DOM 移除
    } else {
      alert("刪除失敗");
    }
  });

  return form;
}
function renderHeader(product, showFields) {
  const section = document.createElement("div");
  section.className = "mb-4 pb-3 border-bottom";

  const headerContent = document.createElement("div");
  headerContent.className = "d-flex flex-wrap align-items-center gap-3 mb-2";
  headerContent.innerHTML = `
    <div class="me-auto d-flex align-items-center gap-3 flex-wrap">
      <h5 class="mb-0 text-primary fw-bold">#${product.id}</h5>

      ${showFields.includes("stall_name") ? `
        <div class="d-flex align-items-center">
          <label class="form-label mb-0 me-2 text-muted">檔口</label>
          <input name="stall_name" class="form-control form-control-sm border-0 bg-light" 
                 style="width: 120px" value="${product.stall_name || ""}">
        </div>` : ""}

      ${showFields.includes("source") ? `
        <div class="d-flex align-items-center">
          <label class="form-label mb-0 me-2 text-muted">來源</label>
          <input name="source" class="form-control form-control-sm border-0 bg-light" 
                 style="width: 120px" value="${product.source || ""}">
        </div>` : ""}

      ${showFields.includes("source_url") ? `
        <div class="d-flex align-items-center">
          <label class="form-label mb-0 me-2 text-muted">網址</label>
          <input name="source_url" class="form-control form-control-sm border-0 bg-light" 
                 style="width: 200px" value="${product.source_url || ""}">
        </div>` : ""}
    </div>

    <div class="d-flex gap-2">
      <button type="submit" class="btn btn-primary btn-sm px-3">儲存</button>
      <button type="button" class="btn btn-outline-danger btn-sm px-3 delete-btn">刪除</button>
    </div>
  `;
  section.appendChild(headerContent);

  if (showFields.includes("name")) {
    const nameRow = document.createElement("div");
    nameRow.className = "mt-3";
    nameRow.innerHTML = `
      <input name="name" class="form-control form-control-lg border-0 bg-light"
             placeholder="商品名稱" value="${product.name || ""}">
    `;
    section.appendChild(nameRow);
  }

  return section;
}



function renderLeftPanel(product, showFields) {
  const container = document.createElement("div");
  container.className = "bg-light rounded-3 p-3 d-flex flex-column gap-3";

  // 價格區塊（訂購價、總成本、價格）
  const priceRow = document.createElement("div");
  priceRow.className = "row g-3";

  priceRow.innerHTML = `
    <div class="col-4">
      <label class="form-label text-muted small">訂購價</label>
      <input name="purchase_price" type="number" class="form-control border-0 bg-white"
             value="${product.purchase_price || ""}">
    </div>
    <div class="col-4">
      <label class="form-label text-muted small">總成本</label>
      <input name="total_cost" type="number" class="form-control border-0 bg-white"
             value="${product.total_cost || ""}">
    </div>
    <div class="col-4">
      <label class="form-label text-muted small">售價</label>
      <input name="price" type="number" class="form-control border-0 bg-white"
             value="${product.price || ""}">
    </div>
  `;
  container.appendChild(priceRow);

  // 商品描述
  if (showFields.includes("description")) {
    const description = document.createElement("div");
    description.innerHTML = `
      <label class="form-label text-muted small">商品描述</label>
      <textarea name="description" class="form-control border-0 bg-white" rows="3"
                placeholder="請輸入商品描述...">${product.description || ""}</textarea>
    `;
    container.appendChild(description);
  }

  // 商品類別（select）
  const typeSelect = document.createElement("div");
  typeSelect.innerHTML = `
    <label class="form-label text-muted small">商品類別</label>
    <select name="custom_type" class="form-select border-0 bg-white">
      <option value="">請選擇</option>
      ${Object.entries(CUSTOM_TYPE_OPTIONS).map(([value, label]) => `
        <option value="${value}" ${product.custom_type === value ? "selected" : ""}>${label}</option>
      `).join("")}
    </select>
  `;
  container.appendChild(typeSelect);

  // 材質
  const material = document.createElement("div");
  material.innerHTML = `
    <label class="form-label text-muted small">材質</label>
    <input name="material" class="form-control border-0 bg-white"
           value="${product.material || ""}">
  `;
  container.appendChild(material);

  // // 尺寸描述
  // const sizeNote = document.createElement("div");
  // sizeNote.innerHTML = `
  //   <label class="form-label text-muted small">尺寸描述</label>
  //   <input name="size_note" class="form-control border-0 bg-white"
  //          value="${product.size_note || ""}">
  // `;
  // container.appendChild(sizeNote);

  // 尺寸欄位（Key-Value 格式）
  const sizeMetricsWidget = createDynamicKVInput("size_metrics", product.size_metrics || {});
  sizeMetricsWidget.id = "size-metrics-widget";
  container.appendChild(sizeMetricsWidget);

  // 顏色欄位（List 格式）
  const colorsWidget = createDynamicListInput("colors", product.colors || []);
  colorsWidget.id = "colors-widget";
  container.appendChild(colorsWidget);

  // 尺寸欄位（List 格式）
  const sizesWidget = createDynamicListInput("sizes", product.sizes || []);
  sizesWidget.id = "sizes-widget";
  container.appendChild(sizesWidget);

  return container;
}

