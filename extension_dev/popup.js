// 當頁面載入時獲取當前 tab 的 URL 和緩存的表單數據
chrome.tabs.query({active: true, currentWindow: true}, async function(tabs) {
  if (tabs[0] && tabs[0].url) {
    document.querySelector('[name="source_url"]').value = tabs[0].url;
  }
  
  // 載入緩存的表單數據
  const form = document.getElementById("product-form");
  const formFields = form.elements;
  const data = await chrome.storage.local.get('formData');
  
  if (data.formData) {
    Object.keys(data.formData).forEach(key => {
      if (formFields[key]) {
        formFields[key].value = data.formData[key];
      }
    });
  }

  // 監聽所有輸入欄位的變化並保存到緩存
  form.addEventListener('input', async function(e) {
    const formData = new FormData(form);
    const data = {};
    for (const [key, value] of formData.entries()) {
      data[key] = value;
    }
    await chrome.storage.local.set({ formData: data });
  });
});

document.getElementById("product-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const form = e.target;
  const msg = document.getElementById("status-msg");
  
  const formData = new FormData(form);
  const data = {};
  
  // 只收集有值的欄位
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
        // 如果 JSON 格式錯誤，仍然繼續處理其他欄位
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
      
      // 清除緩存的表單數據
      await chrome.storage.local.remove('formData');
      
      // 重置表單
      form.reset();
      
      // 重新設定當前網址
      chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        if (tabs[0] && tabs[0].url) {
          document.querySelector('[name="source_url"]').value = tabs[0].url;
        }
      });
    } else {
      const json = await res.json();
      showError(json.detail || "❌ 發生錯誤");
    }
  } catch (err) {
    showError(`🚫 無法連線到伺服器：${err.message}`);
  }
});

function showError(message) {
  const msg = document.getElementById("status-msg");
  msg.textContent = message;
  msg.className = "text-danger text-center mt-2 small";
}

// 載入和保存開關狀態
document.addEventListener('DOMContentLoaded', async () => {
  const toggle = document.getElementById('extensionToggle');
  const data = await chrome.storage.local.get('extensionEnabled');
  toggle.checked = data.extensionEnabled !== false; // 預設為開啟

  toggle.addEventListener('change', async () => {
    await chrome.storage.local.set({ extensionEnabled: toggle.checked });
    // 通知 content script 狀態改變
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (tab) {
      chrome.tabs.sendMessage(tab.id, { 
        type: 'toggleExtension',
        enabled: toggle.checked 
      });
    }
  });
});
