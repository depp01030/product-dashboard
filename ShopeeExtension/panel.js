// 面板 JavaScript: 處理表單功能與資料交互

document.addEventListener('DOMContentLoaded', function() {
  const form = document.getElementById('product-form');
  const statusMsg = document.getElementById('status-msg');
  const closeBtn = document.getElementById('closePanel');
  
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
  
  // 表單提交
  form.addEventListener('submit', async function(e) {
    e.preventDefault();
    statusMsg.textContent = "⏳ 送出中...";
    statusMsg.className = "text-center mt-2 small text-muted";
    
    const data = {};
    const formData = new FormData(form);
    
    for (const [key, value] of formData.entries()) {
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
    
    try {
      const response = await fetch('http://localhost:8000/admin/products/create', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      });
      
      if (response.ok) {
        statusMsg.textContent = "✅ 成功送出！";
        statusMsg.className = "text-center mt-2 small text-success";
        
        // 清空表單和儲存的數據
        form.reset();
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