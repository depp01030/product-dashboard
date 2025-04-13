// 📁 static/js/utils/render-card.js
import { renderImageModule } from "./render-image-module.js";
import { initResizable } from "./resizable-layout.js";

const CUSTOM_TYPE_OPTIONS = {
  top: "女性上著",
  bottom: "女性下著",
  dress: "洋裝",
  coat: "外套",
  skirt: "裙子",
  pants: "褲子",
  accessories: "配飾",
  scarf: "圍巾",
  other: "其他"
};

const SIZE_METRICS_BY_TYPE = {
  top: ["shoulder", "bust", "length", "sleeve"],
  bottom: ["waist", "hip", "length", "inseam"],
  dress: ["shoulder", "bust", "waist", "length"],
  coat: ["shoulder", "bust", "length", "sleeve"],
  skirt: ["waist", "hip", "length"],
  pants: ["waist", "hip", "length", "inseam"],
  accessories: [],
  scarf: ["length"],
  other: []
};

const SIZE_METRIC_LABELS = {
  shoulder: "肩寬",
  bust: "胸圍",
  waist: "腰圍",
  hip: "臀圍",
  length: "衣長",
  sleeve: "袖長",
  inseam: "內檔長"
};

export function renderProductCard(product, options = {}) {
  const {
    showFields = [],
    submitPath = "/admin/products",
    renderAsCheckbox = false
  } = options;

  const form = document.createElement("form");
  form.method = "post";
  form.action = `${submitPath}/${product.id}/update`;
  form.className = "card shadow border-0 mb-4 bg-white";  // 加強陰影效果

  // 添加一個視覺分隔的上邊框
  const borderTop = document.createElement("div");
  borderTop.className = "border-top border-4 border-primary rounded-top";
  form.appendChild(borderTop);

  const cardBody = document.createElement("div");
  cardBody.className = "card-body p-4";  // 增加內部間距

  // === 上方：基本信息 ===
  const headerSection = document.createElement("div");
  headerSection.className = "mb-4 pb-3 border-bottom"; // 增加下方間距
  
  const headerContent = document.createElement("div");
  headerContent.className = "d-flex flex-wrap align-items-center gap-3 mb-2";
  headerContent.innerHTML = `
    <div class="me-auto d-flex align-items-center gap-3">
      <h5 class="mb-0 text-primary fw-bold">#${product.id}</h5>
      ${showFields.includes("stall_name") ? `
        <div class="d-flex align-items-center">
          <label class="form-label mb-0 me-2 text-muted">檔口</label>
          <input name="stall_name" class="form-control form-control-sm border-0 bg-light" 
                 style="width: 120px" value="${product.stall_name || ""}">
        </div>
      ` : ""}
      ${showFields.includes("source") ? `
        <div class="d-flex align-items-center">
          <label class="form-label mb-0 me-2 text-muted">來源</label>
          <input name="source" class="form-control form-control-sm border-0 bg-light" 
                 style="width: 120px" value="${product.source || ""}">
        </div>
      ` : ""}
    </div>
    <div class="d-flex gap-2">
      <button type="submit" class="btn btn-primary btn-sm px-3">儲存</button>
    </div>
  `;
  headerSection.appendChild(headerContent);

  // 商品名稱單獨一行，給予更多空間
  if (showFields.includes("name")) {
    const nameRow = document.createElement("div");
    nameRow.className = "mt-3";
    nameRow.innerHTML = `
      <input name="name" class="form-control form-control-lg border-0 bg-light" 
             placeholder="商品名稱" value="${product.name || ""}">
    `;
    headerSection.appendChild(nameRow);
  }

  cardBody.appendChild(headerSection);

  // === 主要內容區域 ===
  const contentContainer = document.createElement("div");
  contentContainer.className = "resizable-container"; // 改用resizable布局

  // === 左側區域 ===
  const colLeft = document.createElement("div");
  colLeft.className = "resizable-left";  // 改用resizable布局

  // --- 左側上方：預覽圖 ---
  const previewSection = document.createElement("div");
  previewSection.className = "mb-4";
  previewSection.innerHTML = `
    <div class="d-flex gap-3">
      ${(product.image_list || []).slice(0, 3).map(img => `
        <div class="preview-image-wrapper" style="width: 120px;">
          <div class="ratio ratio-1x1">
            <img src="/candidate_images/${encodeURIComponent(product.image_dir)}/${encodeURIComponent(img.filename)}" 
                 class="img-thumbnail object-fit-cover rounded-3 border-0 shadow-sm">
          </div>
        </div>
      `).join("")}
    </div>
  `;
  colLeft.appendChild(previewSection);

  // --- 左側下方：其他信息 ---
  const infoSection = document.createElement("div");
  infoSection.className = "bg-light rounded-3 p-3";  // 添加背景色和圓角
  
  // 商品類別選擇（影響尺寸欄位）
  const customTypeSelect = `
    <div class="mb-3">
      <label class="form-label text-muted small">商品類別</label>
      <select name="custom_type" class="form-select border-0 bg-white" 
              onchange="updateSizeMetrics(this)">
        <option value="">請選擇</option>
        ${Object.entries(CUSTOM_TYPE_OPTIONS).map(([value, label]) => `
          <option value="${value}" ${product.custom_type === value ? 'selected' : ''}>
            ${label}
          </option>
        `).join('')}
      </select>
    </div>
  `;

  // 準備尺寸資訊
  const currentMetrics = product.size_metrics || {};
  const currentType = product.custom_type || '';
  const metricsToShow = SIZE_METRICS_BY_TYPE[currentType] || [];
  
  const sizeMetricsHtml = metricsToShow.length ? `
    <div class="mb-3">
      <label class="form-label text-muted small">尺寸資訊</label>
      <div class="row g-2">
        ${metricsToShow.map(metric => `
          <div class="col-6 col-md-3">
            <div class="input-group input-group-sm">
              <span class="input-group-text border-0 bg-white">${SIZE_METRIC_LABELS[metric]}</span>
              <input type="text" 
                     class="form-control border-0 bg-white" 
                     name="size_metrics_${metric}"
                     value="${currentMetrics[metric] || ''}"
                     placeholder="cm">
            </div>
          </div>
        `).join('')}
      </div>
    </div>
  ` : '';

  infoSection.innerHTML = `
    ${showFields.includes("description") ? `
      <div class="mb-3">
        <label class="form-label text-muted small">商品描述</label>
        <textarea name="description" class="form-control border-0 bg-white" rows="3"
                  placeholder="請輸入商品描述...">${product.description || ""}</textarea>
      </div>
    ` : ""}
    
    ${customTypeSelect}
    ${sizeMetricsHtml}
    
    <div class="row g-3">
      ${showFields.includes("price") ? `
        <div class="col-6">
          <label class="form-label text-muted small">價格</label>
          <div class="input-group">
            <span class="input-group-text border-0 bg-white">NT$</span>
            <input name="price" type="number" class="form-control border-0 bg-white" 
                   value="${product.price || ""}">
          </div>
        </div>
      ` : ""}
      
      ${showFields.includes("material") ? `
        <div class="col-6">
          <label class="form-label text-muted small">材質</label>
          <input name="material" class="form-control border-0 bg-white" 
                 value="${product.material || ""}">
        </div>
      ` : ""}
      
      ${showFields.includes("colors") ? `
        <div class="col-6">
          <label class="form-label text-muted small">顏色</label>
          <input name="colors" class="form-control border-0 bg-white" 
                 value="${(product.colors || []).join(", ")}"
                 placeholder="以逗號分隔">
        </div>
      ` : ""}
      
      ${showFields.includes("sizes") ? `
        <div class="col-6">
          <label class="form-label text-muted small">尺寸</label>
          <input name="sizes" class="form-control border-0 bg-white" 
                 value="${(product.sizes || []).join(", ")}"
                 placeholder="以逗號分隔">
        </div>
      ` : ""}
      
      ${showFields.includes("stock") ? `
        <div class="col-6">
          <label class="form-label text-muted small">庫存</label>
          <input name="stock" type="number" class="form-control border-0 bg-white" value="${product.stock || ""}">
        </div>
      ` : ""}
    </div>
    ${showFields.includes("item_status") ? (
      renderAsCheckbox ? `
        <div class="form-check mt-3">
          <input class="form-check-input" type="checkbox" name="item_status" 
                 id="check-status-${product.id}" value="product" 
                 ${product.item_status === "product" ? "checked" : ""}>
          <label class="form-check-label" for="check-status-${product.id}">
            標記為「已選」
          </label>
          <input type="hidden" name="item_status_unchecked" value="candidate">
        </div>
      ` : `
        <div class="mt-3">
          <label class="form-label text-muted small">商品狀態</label>
          <select name="item_status" class="form-select border-0 bg-white">
            ${generateItemStatusOptions(product.item_status)}
          </select>
        </div>
      `)
    : ""}
  `;
  colLeft.appendChild(infoSection);

  // === 分隔條 ===
  const splitter = document.createElement("div");
  splitter.className = "resizable-splitter";
  
  // === 右側區域 ===
  const colRight = document.createElement("div");
  colRight.className = "resizable-right";  // 改用resizable布局
  colRight.appendChild(renderImageModule(product));

  // 組裝resizable布局
  contentContainer.appendChild(colLeft);
  contentContainer.appendChild(splitter);
  contentContainer.appendChild(colRight);

  cardBody.appendChild(contentContainer);
  form.appendChild(cardBody);

  // 初始化resizable功能
  initResizable(contentContainer);

  // === 表單提交處理 ===
  form.addEventListener("submit", async e => {
    e.preventDefault();
    const formData = new FormData(form);
    if (renderAsCheckbox && !formData.has("item_status")) {
      formData.set("item_status", "candidate");
    }

    // 收集選中的圖片和主圖信息
    const selectedImages = [];
    const mainImage = formData.get("main_image") || "";
    form.querySelectorAll('.image-checkbox:checked').forEach(checkbox => {
      selectedImages.push(checkbox.value);
    });
    formData.set("selected_images", selectedImages.join(","));

    // 收集尺寸資訊
    const sizeMetrics = {};
    const type = formData.get("custom_type");
    if (type && SIZE_METRICS_BY_TYPE[type]) {
      SIZE_METRICS_BY_TYPE[type].forEach(metric => {
        const value = formData.get(`size_metrics_${metric}`);
        if (value) sizeMetrics[metric] = value;
      });
    }
    formData.set("size_metrics", JSON.stringify(sizeMetrics));

    const button = form.querySelector("button[type=submit]");
    button.disabled = true;
    button.innerHTML = `<span class="spinner-border spinner-border-sm me-1"></span> 儲存中...`;

    const res = await fetch(form.action, {
      method: "POST",
      body: formData
    });
    
    if (res.ok) {
      button.className = "btn btn-success btn-sm px-3";
      button.innerHTML = `<i class="bi bi-check2"></i> 已儲存`;
    } else {
      button.className = "btn btn-danger btn-sm px-3";
      button.innerHTML = `<i class="bi bi-x-lg"></i> 儲存失敗`;
    }
    setTimeout(() => {
      button.className = "btn btn-primary btn-sm px-3";
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
