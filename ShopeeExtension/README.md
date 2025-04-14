# Shopee 商品卡片工具 Chrome 擴充功能

一個便捷的 Chrome 擴充功能，可在任意網站上快速開啟商品表單卡片，輸入商品資料並送出到後端。

## 特點

- 🚀 在任何網站一鍵開啟浮動商品表單
- 💾 自動保存表單資料，關閉後再次打開仍保留
- 📱 響應式設計，適應不同屏幕尺寸
- 🔄 無需跳轉頁面或開新標籤頁
- 🔌 直接提交資料到 FastAPI 後端

## 技術實現

本擴充功能基於 Chrome Extension Manifest V3 開發，解決了內容安全策略（CSP）限制問題。

### 核心組件

1. **Background Script** (`background.js`): 
   - 處理擴充功能圖標點擊事件
   - 將訊息傳遞給內容腳本

2. **Content Script** (`content.js`): 
   - 接收背景腳本的訊息
   - 在頁面中注入/移除 iframe 面板
   - 與 iframe 通信以傳遞數據

3. **Panel Page** (`panel.html`, `panel.js`, `panel.css`): 
   - 實現商品表單 UI
   - 處理表單資料的儲存與提交
   - 透過 `chrome.storage.local` API 實現資料暫存

### 技術突破

- 使用 `web_accessible_resources` 聲明可訪問資源
- 透過 `postMessage` API 實現 iframe 與內容腳本間的安全通信
- 避免了 Chrome 封鎖內嵌擴充功能頁面的問題

## 安裝方法

1. 打開 Chrome 瀏覽器，進入 `chrome://extensions/`
2. 開啟右上角「開發者模式」
3. 點擊「載入未封裝項目」
4. 選擇本擴充功能資料夾

## 使用方法

1. 在任意網站點擊擴充功能圖標
2. 填寫商品資訊
3. 點擊「送出」提交資料
4. 關閉面板可用「X」按鈕或按下 ESC 鍵 