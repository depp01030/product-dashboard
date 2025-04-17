// =================== static/js/utils/dom/render-image-module.js ===================

export function renderImageModule(product) {
  const imagePrefix = `/products_root/${encodeURIComponent(product.item_folder)}/`;
  const allImages      = Array.isArray(product.image_list)      ? product.image_list      : [];
  const selectedImages = Array.isArray(product.selected_images) ? product.selected_images : [];
  // 🔹 加在下一行 —— 把它變成 Set 供快速判斷
  const selectedSet = new Set(selectedImages);

  const wrapper = document.createElement("div");
  wrapper.className = "image-module h-100 d-flex flex-column";
  const collapseId = `img-group-${product.id}`;

  /* ---------------- Toolbar ---------------- */
  const toolbar = document.createElement("div");
  toolbar.className = "d-flex justify-content-between align-items-center mb-3";

  const ctrlLeft = document.createElement("div");
  ctrlLeft.className = "d-flex align-items-center gap-2";

  const toggleBtn = document.createElement("button");
  toggleBtn.type  = "button";
  toggleBtn.className = "btn btn-light btn-sm text-muted";
  toggleBtn.dataset.bsToggle = "collapse";
  toggleBtn.dataset.bsTarget = `#${collapseId}`;
  toggleBtn.innerHTML = `<div class='d-flex align-items-center gap-2'><i class='bi bi-images'></i><span>全部圖片</span><span class='badge bg-secondary rounded-pill'>${allImages.length}</span></div>`;
  ctrlLeft.appendChild(toggleBtn);

  /* ---- 匯入照片 ---- */
  const importLabel = document.createElement("label");
  importLabel.className = "btn btn-outline-primary btn-sm mb-0 d-flex align-items-center gap-1";
  const cap = document.createElement("span");
  cap.textContent = "匯入照片";
  importLabel.appendChild(cap);
  const fileInput = document.createElement("input");
  fileInput.type = "file";
  fileInput.name = "image_import";
  fileInput.multiple = true;
  fileInput.hidden = true;
  importLabel.appendChild(fileInput);
  ctrlLeft.appendChild(importLabel);

  /* ---- 資料夾連結 ---- */
  const folderBtn = document.createElement("button");
  folderBtn.type = "button";
  folderBtn.className = "btn btn-light btn-sm";
  folderBtn.textContent = `資料夾：${product.item_folder}`;
  folderBtn.addEventListener("click", ()=>window.open(`/candidate_images/${encodeURIComponent(product.item_folder)}/`,"_blank"));
  ctrlLeft.appendChild(folderBtn);

  /* 已選數量 */
  const selBadge = document.createElement("span");
  selBadge.className = "badge bg-primary rounded-pill";
  selBadge.textContent = `已選: ${selectedImages.length}`;

  toolbar.appendChild(ctrlLeft);
  toolbar.appendChild(selBadge);
  wrapper.appendChild(toolbar);

  /* ---------------- Collapse + Grid ---------------- */
  const collapse = document.createElement("div");
  collapse.id = collapseId;
  collapse.className = "collapse flex-grow-1";
  const scroller  = document.createElement("div");
  scroller.className = "bg-light rounded-3 p-3";
  const grid = document.createElement("div");
  grid.className = "row g-3";
  scroller.appendChild(grid);
  collapse.appendChild(scroller);
  wrapper.appendChild(collapse);

  /*  util: 刷新 badge  */
  const refreshBadge = ()=>{
    const cnt = wrapper.querySelectorAll(".image-checkbox:checked").length + (wrapper.tempFiles?wrapper.tempFiles.filter(f=>f._checked).length:0);
    selBadge.textContent = `已選: ${cnt}`;
  };

  /* ----------- 現有圖片卡 ----------- */
  const addImageCard = (filename,isTemp,fileObj)=>{
    const col  = document.createElement("div");
    col.className = "col-4";

    const card = document.createElement("div");
    card.className = "card h-100 border-0 shadow-sm image-item" + (isTemp?" selected":"");

    const imgBox = document.createElement("div");
    imgBox.className = "ratio ratio-1x1";
    const img = document.createElement("img");
    img.className = "card-img-top object-fit-cover rounded-top";
    if(isTemp){
      const url = URL.createObjectURL(fileObj);
      img.src = url;
      img.onload = ()=>URL.revokeObjectURL(url);
    }else{
      img.src = imagePrefix + encodeURIComponent(filename);
      img.loading = "lazy";
    }
    imgBox.appendChild(img);
    card.appendChild(imgBox);

    /* footer controls */
    const footer = document.createElement("div");
    footer.className = "card-footer bg-white border-0 p-2 d-flex justify-content-between align-items-center gap-2";

    // left: checkbox & (可設定主圖)
    const boxLeft = document.createElement("div");
    boxLeft.className = "d-flex align-items-center gap-2";
    const chk = document.createElement("input");
    chk.type = "checkbox";
    chk.className = isTemp?"form-check-input temp-checkbox":"form-check-input image-checkbox";
    chk.name = isTemp?"temp_selected":"selected_images[]";
    chk.value = filename;
    if(isTemp) chk.checked = true;
    // ❷  在 addImageCard 建立 checkbox 之後，插入下面這段
    if (selectedSet.has(filename)) {
      chk.checked = true;              // 勾選
      card.classList.add("selected");  // 加藍框
    }
    boxLeft.appendChild(chk);

    const lab = document.createElement("label");
    lab.className = "small";
    lab.textContent = "選擇";
    boxLeft.appendChild(lab);

    const radio = document.createElement("input");
    radio.type = "radio";
    radio.className = "form-check-input";
    radio.name = "main_image";
    radio.value = filename;
    if(!isTemp && product.main_image===filename) radio.checked = true;
    boxLeft.appendChild(radio);

    footer.appendChild(boxLeft);

    // right: 刪除按鈕
    const delBtn = document.createElement("button");
    delBtn.type = "button";
    delBtn.className = "btn btn-sm btn-outline-danger";
    delBtn.innerHTML = "<i class='bi bi-trash'></i>";
    footer.appendChild(delBtn);

    card.appendChild(footer);
    col.appendChild(card);
    isTemp?grid.prepend(col):grid.appendChild(col);

    /* 事件 */
    chk.addEventListener("change",()=>{
      if(isTemp) fileObj._checked = chk.checked;
      card.classList.toggle("selected",chk.checked);
      refreshBadge();
    });
    radio.addEventListener("change",()=>{
      if(radio.checked) scroller.querySelectorAll(".image-item").forEach(c=>c.classList.remove("is-main"));
      if(radio.checked) card.classList.add("is-main");
    });
    delBtn.addEventListener("click",async()=>{
      if(isTemp){
        wrapper.tempFiles = wrapper.tempFiles.filter(f=>f!==fileObj);
        col.remove();
        refreshBadge();
      }else{
        if(!confirm(`確定刪除 ${filename} 嗎?`)) return;
        const res = await fetch(`/admin/products/${product.id}/images/${encodeURIComponent(filename)}`,{method:"DELETE"});
        if(res.ok) col.remove();
      }
    });
  };

  /* 既有圖片 */
  allImages.forEach(img=>addImageCard(img.filename,false));

  /* ----------- 匯入 change ----------- */
  // ---------- 匯入圖片即時預覽 ---------- //
  fileInput.addEventListener("change", () => {
    if (!fileInput.files.length) return;
    wrapper.tempFiles = wrapper.tempFiles || [];

    [...fileInput.files].forEach(file => {
      file._checked = false;                // 預設不打勾
      wrapper.tempFiles.push(file);

      const col   = document.createElement("div");
      col.className = "col-4";

      const card  = document.createElement("div");
      card.className = "card h-100 border-0 shadow-sm image-item";

      const box   = document.createElement("div");
      box.className = "ratio ratio-1x1";
      const img    = document.createElement("img");
      const url    = URL.createObjectURL(file);
      img.src      = url;
      img.className = "card-img-top object-fit-cover rounded-top";
      img.onload   = () => URL.revokeObjectURL(url);
      box.appendChild(img);
      card.appendChild(box);

      const controls = document.createElement("div");
      controls.className = "card-footer bg-white border-0 p-2";
      controls.innerHTML = `<div class='d-flex justify-content-between align-items-center gap-2'>\
        <div class='form-check mb-0'>\
          <input class='form-check-input temp-checkbox' type='checkbox'>\
          <label class='form-check-label small'>選擇</label>\
        </div>\
        <div class='form-check mb-0'>\
          <input class='form-check-input' type='radio' name='main_image' value='${file.name}'>\
          <label class='form-check-label small'>主圖</label>\
        </div>\
      </div>`;
      card.appendChild(controls);
      col.appendChild(card);
      grid.prepend(col);

      // checkbox 控制標註
      const tcb = controls.querySelector(".temp-checkbox");
      tcb.addEventListener("change", () => {
        file._checked = tcb.checked;
        card.classList.toggle("selected", tcb.checked);
        refreshBadge();
      });

      // radio 設主圖
      const rd = controls.querySelector("input[type=radio]");
      rd.addEventListener("change", () => {
        if (rd.checked) scroller.querySelectorAll(".image-item").forEach(c => c.classList.remove("is-main"));
        if (rd.checked) card.classList.add("is-main");
      });
    });

    // 更新 badge & 總數
    const totalBadge = toggleBtn.querySelector(".badge");
    totalBadge.textContent = parseInt(totalBadge.textContent, 10) + fileInput.files.length;
    refreshBadge();
    bootstrap.Collapse.getOrCreateInstance(collapse).show();
  });

  return wrapper;
}

