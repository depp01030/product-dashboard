// 背景 Service Worker：處理擴充功能圖標點擊事件

// 監聽擴充功能圖標點擊
chrome.action.onClicked.addListener(async (tab) => {
  try {
    // 傳送消息到 content script 以切換面板顯示狀態
    await chrome.tabs.sendMessage(tab.id, { action: "togglePanel" });
  } catch (error) {
    console.error("Error sending message to content script:", error);
    
    // 如果 content script 尚未載入，則嘗試執行注入
    await chrome.scripting.executeScript({
      target: { tabId: tab.id },
      files: ["content.js"]
    });
    
    // 注入 CSS
    await chrome.scripting.insertCSS({
      target: { tabId: tab.id },
      files: ["content.css"]
    });
    
    // 再次嘗試發送消息
    setTimeout(async () => {
      await chrome.tabs.sendMessage(tab.id, { action: "togglePanel" });
    }, 100);
  }
}); 