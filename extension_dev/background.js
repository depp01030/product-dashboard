// 背景 script：控制點擊 icon 時的 iframe 注入/移除行為

chrome.action.onClicked.addListener(async (tab) => {
    await chrome.scripting.executeScript({
      target: { tabId: tab.id },
      func: toggleExtensionPanel
    });
  });
  
  function toggleExtensionPanel() {
    const existing = document.querySelector("#shopee-extension-panel");
    if (existing) {
      existing.remove(); // 已存在 → 移除
      return;
    }
  
    const iframe = document.createElement("iframe");
    iframe.src = chrome.runtime.getURL("popup.html");
    iframe.id = "shopee-extension-panel";
    iframe.style.cssText = `
      position: fixed;
      top: 80px;
      right: 20px;
      width: 360px;
      height: 90%;
      z-index: 9999;
      box-shadow: 0 0 10px rgba(0,0,0,0.15);
      border: none;
      border-radius: 8px;
      background: white;
    `;
    document.body.appendChild(iframe);
  }
  