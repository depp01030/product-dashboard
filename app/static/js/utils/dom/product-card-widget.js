// 📁 static/js/utils/dom/product-card-widget.js

/**
 * 動態 List 欄位生成器（如：colors、sizes）
 */
export function createDynamicListInput(name, initialValues = []) {
    const container = document.createElement("div");
    container.className = "dynamic-list-input d-flex flex-column gap-2";
  
    const label = document.createElement("label");
    label.className = "form-label text-muted small";
    label.textContent = name === "colors" ? "顏色（可多選）" : name === "sizes" ? "尺寸（可多選）" : name;
    container.appendChild(label);
  
    const addButton = document.createElement("button");
    addButton.type = "button";
    addButton.className = "btn btn-outline-secondary btn-sm align-self-start";
    addButton.textContent = "➕ 新增一項";
  
    addButton.addEventListener("click", () => {
      container.insertBefore(createListItem(name, ""), addButton);
    });
  
    container.appendChild(addButton);
  
    initialValues
      .map(v => v.trim())
      .filter(v => v)
      .forEach(val => {
        container.insertBefore(createListItem(name, val), addButton);
      });
  
    return container;
  }
  
  function createListItem(name, value) {
    const wrapper = document.createElement("div");
    wrapper.className = "d-flex gap-2 align-items-center";
  
    const input = document.createElement("input");
    input.name = `${name}[]`;
    input.value = value;
    input.className = "form-control form-control-sm";
  
    const removeBtn = document.createElement("button");
    removeBtn.type = "button";
    removeBtn.className = "btn btn-sm btn-outline-danger";
    removeBtn.innerHTML = "<i class='bi bi-x'></i>";
    removeBtn.addEventListener("click", () => wrapper.remove());
  
    wrapper.appendChild(input);
    wrapper.appendChild(removeBtn);
    return wrapper;
  }
  
  export function extractDynamicListValues(container) {
    return Array.from(container.querySelectorAll("input[name$='[]']"))
      .map(input => input.value.trim())
      .filter(v => v);
  }
  
  /**
   * 動態 Key-Value 欄位生成器（如：size_metrics）
   */
  export function createDynamicKVInput(name, initialDict = {}) {
    const container = document.createElement("div");
    container.className = "dynamic-kv-input d-flex flex-column gap-2";
  
    const label = document.createElement("label");
    label.className = "form-label text-muted small";
    label.textContent = "尺寸明細（可自訂欄位名稱）";
    container.appendChild(label);
  
    const addButton = document.createElement("button");
    addButton.type = "button";
    addButton.className = "btn btn-outline-secondary btn-sm align-self-start";
    addButton.textContent = "➕ 新增欄位";
  
    addButton.addEventListener("click", () => {
      container.insertBefore(createKVItem(name, "", ""), addButton);
    });
  
    container.appendChild(addButton); // ✅ 先加上按鈕
  
    Object.entries(initialDict).forEach(([k, v]) => {
      container.insertBefore(createKVItem(name, k, v), addButton);
    });
  
    return container;
  }
  
  function createKVItem(name, key, value) {
    const wrapper = document.createElement("div");
    wrapper.className = "d-flex gap-2 align-items-center";
  
    const keyInput = document.createElement("input");
    keyInput.name = `${name}_key[]`;
    keyInput.placeholder = "欄位名稱";
    keyInput.value = key;
    keyInput.className = "form-control form-control-sm w-25";
  
    const valueInput = document.createElement("input");
    valueInput.name = `${name}_value[]`;
    valueInput.placeholder = "數值";
    valueInput.value = value;
    valueInput.className = "form-control form-control-sm w-50";
  
    const removeBtn = document.createElement("button");
    removeBtn.type = "button";
    removeBtn.className = "btn btn-sm btn-outline-danger";
    removeBtn.innerHTML = "<i class='bi bi-x'></i>";
    removeBtn.addEventListener("click", () => wrapper.remove());
  
    wrapper.appendChild(keyInput);
    wrapper.appendChild(valueInput);
    wrapper.appendChild(removeBtn);
    return wrapper;
  }
  
  export function extractDynamicKVValues(container) {
    const keys = container.querySelectorAll("input[name$='_key[]']");
    const values = container.querySelectorAll("input[name$='_value[]']");
    const result = {};
  
    for (let i = 0; i < keys.length; i++) {
      const k = keys[i].value.trim();
      const v = values[i].value.trim();
      if (k) result[k] = v;
    }
    return result;
  }
  