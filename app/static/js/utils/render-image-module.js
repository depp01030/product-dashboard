// 📁 static/js/utils/render-image-module.js

/**
 * 建立圖片模組（卡片右側）：
 * - 含展開/收合按鈕
 * - 水平滾動區域
 * - lazy loading
 */
export function renderImageModule(product) {
  const imagePrefix = `/candidate_images/${encodeURIComponent(product.image_dir)}/`;
  const allImages = Array.isArray(product.image_list) ? product.image_list : [];
  const selectedImages = Array.isArray(product.selected_images) ? product.selected_images : [];

  const wrapper = document.createElement("div");
  wrapper.className = "image-module h-100 d-flex flex-column";

  const collapseId = `img-group-${product.id}`;

  // === 頂部工具欄 ===
  const toolbar = document.createElement("div");
  toolbar.className = "d-flex justify-content-between align-items-center mb-3";
  
  // 展開/收合按鈕
  const toggleBtn = document.createElement("button");
  toggleBtn.className = "btn btn-light btn-sm text-muted";
  toggleBtn.setAttribute("data-bs-toggle", "collapse");
  toggleBtn.setAttribute("data-bs-target", `#${collapseId}`);
  toggleBtn.type = "button";
  toggleBtn.innerHTML = `
    <div class="d-flex align-items-center gap-2">
      <i class="bi bi-images"></i>
      <span>全部圖片</span>
      <span class="badge bg-secondary rounded-pill">${allImages.length}</span>
    </div>
  `;
  
  // 已選計數器
  const selectionCount = document.createElement("div");
  selectionCount.className = "badge bg-primary rounded-pill";
  selectionCount.textContent = `已選: ${selectedImages.length}`;
  
  toolbar.appendChild(toggleBtn);
  toolbar.appendChild(selectionCount);
  wrapper.appendChild(toolbar);

  // === 圖片列表容器（預設收合） ===
  const collapse = document.createElement("div");
  collapse.className = "collapse flex-grow-1";
  collapse.id = collapseId;

  const scroller = document.createElement("div");
  scroller.className = "bg-light rounded-3 p-3";
  
  const grid = document.createElement("div");
  grid.className = "row g-3";  // 使用網格布局

  allImages.forEach(img => {
    const imgWrapper = document.createElement("div");
    imgWrapper.className = "col-4";  // 改為 col-4，每行三張圖

    const card = document.createElement("div");
    card.className = "card h-100 border-0 shadow-sm image-item";
    
    // 圖片容器
    const imgContainer = document.createElement("div");
    imgContainer.className = "ratio ratio-1x1";
    
    const imgEl = document.createElement("img");
    imgEl.src = imagePrefix + encodeURIComponent(img.filename);
    imgEl.className = "card-img-top object-fit-cover rounded-top";
    imgEl.loading = "lazy";
    imgContainer.appendChild(imgEl);
    card.appendChild(imgContainer);
    
    // 控制項容器
    const controls = document.createElement("div");
    controls.className = "card-footer bg-white border-0 p-2";
    controls.innerHTML = `
      <div class="d-flex justify-content-between align-items-center gap-2">
        <div class="form-check mb-0">
          <input class="form-check-input image-checkbox" type="checkbox" 
                 value="${img.filename}"
                 name="selected_images[]"
                 ${selectedImages.includes(img.filename) ? 'checked' : ''}>
          <label class="form-check-label small">選擇</label>
        </div>
        <div class="form-check mb-0">
          <input class="form-check-input" type="radio" 
                 name="main_image" 
                 value="${img.filename}"
                 ${product.main_image === img.filename ? 'checked' : ''}>
          <label class="form-check-label small">主圖</label>
        </div>
      </div>
    `;

    card.appendChild(controls);
    imgWrapper.appendChild(card);

    // 更新已選計數和視覺效果
    const checkbox = controls.querySelector('.image-checkbox');
    checkbox.addEventListener('change', () => {
      const checkedCount = scroller.querySelectorAll('.image-checkbox:checked').length;
      selectionCount.textContent = `已選: ${checkedCount}`;
      card.classList.toggle('selected', checkbox.checked);
    });

    // 更新主圖狀態的視覺效果
    const radio = controls.querySelector('input[type="radio"]');
    radio.addEventListener('change', () => {
      scroller.querySelectorAll('.image-item').forEach(item => {
        item.classList.remove('is-main');
      });
      if (radio.checked) {
        card.classList.add('is-main');
      }
    });

    // 設置初始狀態
    if (selectedImages.includes(img.filename)) {
      card.classList.add('selected');
    }
    if (product.main_image === img.filename) {
      card.classList.add('is-main');
    }

    grid.appendChild(imgWrapper);
  });

  scroller.appendChild(grid);
  collapse.appendChild(scroller);
  wrapper.appendChild(collapse);

  return wrapper;
}
