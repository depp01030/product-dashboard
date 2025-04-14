// Content Script：處理在頁面中創建和管理面板

// 全局變數儲存面板元素
let productPanel = null;

// 監聽來自 background script 的消息
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "togglePanel") {
    toggleProductPanel();
  }
  return true;
});

// 切換產品面板顯示或隱藏
function toggleProductPanel() {
  if (productPanel) {
    // 如果面板已存在，則移除
    document.body.removeChild(productPanel);
    productPanel = null;
    return;
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
      } else if (event.data.type === 'CLOSE_PANEL' && productPanel) {
        document.body.removeChild(productPanel);
        productPanel = null;
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