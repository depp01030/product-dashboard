// 創建表單容器
function createFormContainer() {
  const container = document.createElement('div');
  container.id = 'shopee-product-form-container';
  container.style.display = 'none'; // 預設隱藏
  container.innerHTML = `
    <div class="form-wrapper">
      <h5 class="mb-3 text-dark">新增商品資料</h5>
      <div class="form-content">
        <form id="product-form">
          <div class="form-group">
            <label class="form-label">檔口名稱</label>
            <input class="form-control" name="stall_name">
          </div>

          <div class="form-group">
            <label class="form-label">商品名稱</label>
            <input class="form-control" name="name">
          </div>

          <div class="form-group">
            <label class="form-label">商品描述</label>
            <textarea class="form-control" name="description" rows="2"></textarea>
          </div>

          <div class="row g-2">
            <div class="col">
              <div class="form-group">
                <label class="form-label">價格</label>
                <input class="form-control" name="price" type="number">
              </div>
            </div>
            <div class="col">
              <div class="form-group">
                <label class="form-label">真實庫存</label>
                <input class="form-control" name="real_stock" type="number">
              </div>
            </div>
          </div>

          <div class="form-group">
            <label class="form-label">來源網址</label>
            <input class="form-control" name="source_url" readonly>
          </div>

          <div class="form-group">
            <label class="form-label">自定分類</label>
            <input class="form-control" name="custom_type">
          </div>

          <div class="form-group">
            <label class="form-label">商品材質</label>
            <input class="form-control" name="material">
          </div>

          <div class="form-group">
            <label class="form-label">尺寸資訊</label>
            <input class="form-control" name="size_metrics" placeholder='{"腰圍":"30"}'>
          </div>

          <div class="form-group">
            <label class="form-label">尺寸描述</label>
            <input class="form-control" name="size_note">
          </div>

          <div class="form-group">
            <label class="form-label">顏色（逗號分隔）</label>
            <input class="form-control" name="colors">
          </div>

          <div class="form-group">
            <label class="form-label">尺寸（逗號分隔）</label>
            <input class="form-control" name="sizes">
          </div>

          <button class="btn btn-primary w-100" type="submit">送出</button>
          <div id="status-msg" class="text-center mt-2 small text-muted"></div>
        </form>
      </div>
    </div>
  `;
  return container;
}

// 創建切換按鈕
function createToggleButton() {
  const button = document.createElement('button');
  button.id = 'shopee-form-toggle';
  button.style.display = 'none'; // 預設隱藏
  button.innerHTML = '➕ 新增商品';
  return button;
}

// 處理開關邏輯
let formContainer = null;
let toggleButton = null;

// 全局變數儲存面板元素
let productPanel = null;

// 初始化函數
async function initializeExtension() {
  // 檢查是否已啟用
  const data = await chrome.storage.local.get('extensionEnabled');
  if (data.extensionEnabled !== false) { // 預設啟用
    setupUI();
  }
}

// 設置 UI 元素
function setupUI() {
  if (!formContainer) {
    formContainer = createFormContainer();
    toggleButton = createToggleButton();
    document.body.appendChild(toggleButton);
    document.body.appendChild(formContainer);
    
    // 初始化事件監聽
    setupEventListeners();
    
    // 設置當前頁面 URL
    document.querySelector('[name="source_url"]').value = window.location.href;
    
    // 載入表單數據
    loadFormData();
  }
  
  toggleButton.style.display = 'block';
}

// 移除 UI 元素
function removeUI() {
  if (formContainer) {
    formContainer.style.display = 'none';
    toggleButton.style.display = 'none';
  }
}

// 監聽來自 popup 的消息
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === 'toggleExtension') {
    if (message.enabled) {
      setupUI();
    } else {
      removeUI();
    }
  }
});

// 監聽來自 background script 的消息
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "togglePanel") {
    toggleProductPanel();
  }
  return true;
});

// 設置事件監聽
function setupEventListeners() {
  toggleButton.addEventListener('click', () => {
    const isVisible = formContainer.style.display !== 'none';
    formContainer.style.display = isVisible ? 'none' : 'block';
    toggleButton.innerHTML = isVisible ? '➕ 新增商品' : '✖ 關閉表單';
  });

  // 監聽表單變化
  document.getElementById("product-form").addEventListener('input', async function(e) {
    const formData = new FormData(e.target);
    const data = {};
    for (const [key, value] of formData.entries()) {
      data[key] = value;
    }
    await chrome.storage.local.set({ formData: data });
  });

  // 處理表單提交
  document.getElementById("product-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const form = e.target;
    const msg = document.getElementById("status-msg");
    
    const formData = new FormData(form);
    const data = {};
    
    for (const [key, value] of formData.entries()) {
      if (!value || (typeof value === 'string' && value.trim() === '')) continue;
      
      if (["price", "real_stock"].includes(key)) {
        const num = Number(value);
        if (!isNaN(num)) {
          data[key] = num;
        }
      } else if (["colors", "sizes"].includes(key)) {
        const items = value.split(",").map(s => s.trim()).filter(s => s);
        if (items.length > 0) {
          data[key] = items;
        }
      } else if (key === "size_metrics" && value.trim()) {
        try {
          const parsed = JSON.parse(value);
          if (Object.keys(parsed).length > 0) {
            data[key] = parsed;
          }
        } catch (err) {
          console.warn('尺寸資訊格式不正確，已略過此欄位');
        }
      } else if (value.trim()) {
        data[key] = value;
      }
    }

    try {
      const res = await fetch("http://localhost:8000/products/create", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      });

      if (res.ok) {
        msg.textContent = "✅ 已成功送出！";
        msg.className = "text-success text-center mt-2 small";
        
        await chrome.storage.local.remove('formData');
        form.reset();
        document.querySelector('[name="source_url"]').value = window.location.href;
      } else {
        const json = await res.json();
        showError(json.detail || "❌ 發生錯誤");
      }
    } catch (err) {
      showError(`🚫 無法連線到伺服器：${err.message}`);
    }
  });
}

// 初始化擴充功能
initializeExtension();

function showError(message) {
  const msg = document.getElementById("status-msg");
  msg.textContent = message;
  msg.className = "text-danger text-center mt-2 small";
}

// 載入已儲存的表單數據
async function loadFormData() {
  const data = await chrome.storage.local.get('formData');
  const form = document.getElementById('product-form');

  if (data.formData) {
    for (const key in data.formData) {
      const input = form.querySelector(`[name="${key}"]`);
      if (input) {
        input.value = data.formData[key];
      }
    }
  }
}

// 切換產品面板顯示或隱藏
function toggleProductPanel() {
  if (productPanel) {
    // 如果面板已存在，則不移除
    return; // Prevent accidental removal
  }
  
  // 創建面板容器
  productPanel = document.createElement('div');
  productPanel.id = 'shopee-product-panel-container';
  
  // 創建 iframe 來載入面板頁面
  const iframe = document.createElement('iframe');
  iframe.id = 'shopee-product-panel-iframe';
  
  // 使用 web_accessible_resources 中聲明的資源
  iframe.src = chrome.runtime.getURL('panel.html');
  
  // 添加 iframe 到面板容器
  productPanel.appendChild(iframe);
  
  // 添加面板到頁面
  document.body.appendChild(productPanel);
  
  // 自動填充當前頁面 URL
  window.addEventListener('message', function(event) {
    // 確保消息來自我們的擴充功能
    if (event.source === iframe.contentWindow) {
      if (event.data.type === 'PANEL_READY') {
        iframe.contentWindow.postMessage({
          type: 'FILL_URL',
          url: window.location.href
        }, '*');
      }
    }
  });
  
  // 設置關閉面板的處理程序
  document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape' && productPanel) {
      document.body.removeChild(productPanel);
      productPanel = null;
    }
  });
}

// 確保面板在滾動時不會消失
window.addEventListener('scroll', function() {
  if (productPanel) {
    productPanel.style.top = `${window.scrollY + 80}px`; // Adjust position based on scroll
  }
});