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
  
    const wrapper = document.createElement("div");
    wrapper.className = "image-module-wrapper position-relative";
  
    const collapseId = `img-group-${product.id}`;
  
    // === 展開收合按鈕 ===
    const toggleBtn = document.createElement("button");
    toggleBtn.className = "btn btn-sm btn-outline-secondary mb-2";
    toggleBtn.setAttribute("data-bs-toggle", "collapse");
    toggleBtn.setAttribute("data-bs-target", `#${collapseId}`);
    toggleBtn.type = "button";
    toggleBtn.textContent = "顯示全部圖片";
    wrapper.appendChild(toggleBtn);
  
    // === 圖片容器（水平 scroll） ===
    const collapse = document.createElement("div");
    collapse.className = "collapse mb-2 show";
    collapse.id = collapseId;
  
    const scroller = document.createElement("div");
    scroller.className = "d-flex flex-nowrap overflow-auto gap-2";
    scroller.style.maxWidth = "100%";
  
    allImages.forEach(img => {
      const imgEl = document.createElement("img");
      imgEl.src = imagePrefix + encodeURIComponent(img.filename);
      imgEl.className = "img-thumbnail";
      imgEl.style.height = "100px";
      imgEl.loading = "lazy"; // ✅ lazy loading
      scroller.appendChild(imgEl);
    });
  
    collapse.appendChild(scroller);
    wrapper.appendChild(collapse);
  
    return wrapper;
  }
  