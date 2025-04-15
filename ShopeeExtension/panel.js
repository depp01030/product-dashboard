// 面板 JavaScript: 處理表單功能與資料交互

document.addEventListener('DOMContentLoaded', function() {
  const form = document.getElementById('product-form');
  const statusMsg = document.getElementById('status-msg');
  const closeBtn = document.getElementById('closePanel');
  const dropZone = document.getElementById('image-drop-zone');
  const imageInput = document.getElementById('image-input');
  const imagePreview = document.getElementById('image-preview');
  let uploadedImages = [];
  
  // 通知內容腳本面板已準備好接收數據
  window.parent.postMessage({ type: 'PANEL_READY' }, '*');
  
  // 接收來自內容腳本的消息
  window.addEventListener('message', function(event) {
    if (event.data.type === 'FILL_URL') {
      document.querySelector('[name="source_url"]').value = event.data.url;
    }
  });
  
  // 載入已儲存的表單數據
  loadFormData();
  
  // 關閉按鈕點擊事件
  closeBtn.addEventListener('click', function() {
    window.parent.postMessage({ type: 'CLOSE_PANEL' }, '*');
  });
  
  // 表單輸入時儲存數據
  form.addEventListener('input', function(e) {
    if (e.target.name) {
      saveFormField(e.target.name, e.target.value);
    }
  });
  
  // 圖片拖放功能
  dropZone.addEventListener('click', () => imageInput.click());
  
  dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('dragover');
  });
  
  dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('dragover');
  });
  
  dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('dragover');
    const files = e.dataTransfer.files;
    handleFiles(files);
  });
  
  imageInput.addEventListener('change', (e) => {
    handleFiles(e.target.files);
  });

  function handleFiles(files) {
    Array.from(files).forEach(file => {
      if (!file.type.startsWith('image/')) return;
      
      const reader = new FileReader();
      reader.onload = (e) => {
        const imageData = e.target.result;
        uploadedImages.push({
          data: imageData,
          file: file
        });
        updateImagePreview();
      };
      reader.readAsDataURL(file);
    });
  }

  function updateImagePreview() {
    imagePreview.innerHTML = '';
    uploadedImages.forEach((image, index) => {
      const preview = document.createElement('div');
      preview.className = 'image-preview';
      preview.innerHTML = `
        <img src="${image.data}" alt="Preview">
        <button type="button" class="remove-image" data-index="${index}">&times;</button>
      `;
      imagePreview.appendChild(preview);
    });

    // 添加刪除按鈕事件
    imagePreview.querySelectorAll('.remove-image').forEach(button => {
      button.addEventListener('click', (e) => {
        const index = parseInt(e.target.dataset.index);
        uploadedImages.splice(index, 1);
        updateImagePreview();
      });
    });
  }
  
  // 表單提交
  form.addEventListener('submit', async function(e) {
    e.preventDefault();
    statusMsg.textContent = "⏳ 送出中...";
    statusMsg.className = "text-center mt-2 small text-muted";
    
    const formData = new FormData();
    const data = {};
    
    for (const [key, value] of new FormData(form).entries()) {
      if (["price", "real_stock"].includes(key)) {
        data[key] = value ? Number(value) : null;
      } else if (["colors", "sizes"].includes(key)) {
        data[key] = value ? value.split(",").map(s => s.trim()) : [];
      } else if (key === "size_metrics" && value.trim()) {
        try {
          data[key] = JSON.parse(value);
        } catch (err) {
          statusMsg.textContent = "❌ 尺寸資訊格式錯誤，請使用正確的 JSON 格式";
          statusMsg.className = "text-center mt-2 small text-danger";
          return;
        }
      } else {
        data[key] = value || null;
      }
    }

    // 添加圖片數據
    uploadedImages.forEach((image, index) => {
      formData.append(`images`, image.file);
    });
    formData.append('data', JSON.stringify(data));
    
    try {
      const response = await fetch('http://localhost:8000/admin/products/create', {
        method: 'POST',
        body: formData
      });
      
      if (response.ok) {
        statusMsg.textContent = "✅ 成功送出！";
        statusMsg.className = "text-center mt-2 small text-success";
        
        // 清空表單和儲存的數據
        form.reset();
        uploadedImages = [];
        updateImagePreview();
        chrome.storage.local.clear();
      } else {
        const errorData = await response.json();
        statusMsg.textContent = "❌ 錯誤：" + (errorData.detail || "未知錯誤");
        statusMsg.className = "text-center mt-2 small text-danger";
      }
    } catch (error) {
      statusMsg.textContent = "🚫 無法連線到伺服器: " + error.message;
      statusMsg.className = "text-center mt-2 small text-danger";
    }
  });
});

// 儲存單個表單欄位
function saveFormField(name, value) {
  chrome.storage.local.set({ [name]: value });
}

// 載入所有已儲存的表單數據
async function loadFormData() {
  const form = document.getElementById('product-form');
  
  for (const input of form.elements) {
    if (input.name) {
      try {
        const data = await chrome.storage.local.get(input.name);
        if (data[input.name]) {
          input.value = data[input.name];
        }
      } catch (error) {
        console.error("無法載入已儲存的資料:", error);
      }
    }
  }
} 