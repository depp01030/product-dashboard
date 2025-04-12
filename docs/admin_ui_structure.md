
# 🧠 Shopee 後台頁面系統結構說明（Admin UI Structure）

本文件說明 Shopee 上架系統後台的頁面結構、功能分工、資料流動與維護策略，設計以「模組化、可擴充、避免重複程式碼」為目標。

---

## 📁 頁面總覽與目的

| 頁面       | URL 路徑              | 顯示內容 |
|------------|-----------------------|----------|
| candidates | `/admin/candidates`   | 顯示候選商品：檔口、ID、名稱、狀態、圖片 |
| products   | `/admin/products`     | 已選商品（包含描述、價格、顏色、尺寸等） |
| stocks     | `/admin/stocks`       | 商品庫存管理（多出庫存欄位） |
| account    | `/admin/account`      | 報表分析（結構待規劃） |

---

## 🧱 檔案架構設計

### HTML Templates（Jinja2 繼承）

templates/admin/
├── base_list.html           # 共用骨架  
├── candidates_page.html     # 各頁繼承 base_list  
├── products_page.html  
├── stocks_page.html  
└── account_page.html  

### JavaScript 模組化

static/js/  
├── pages/                   # 每頁主控 JS  
│   ├── candidates_page.js  
│   ├── products_page.js  
│   ├── stocks_page.js  
│   └── account_page.js  
└── modules/                 # 共用模組  
    ├── data_loader.js       # API 請求 / 分頁邏輯  
    ├── card_renderer.js     # 根據欄位渲染卡片  
    └── image_module.js      # lazy loading / 勾選主圖  

### FastAPI Routes

api/  
├── admin_pages.py           # 每頁回傳 HTML 頁面  
└── admin_api.py             # 共用資料 API 查詢（含篩選）  

---

## 🔁 資料查詢 API 設計

共用 `/admin/api/products` 路由，使用 query string 區分邏輯。

| 頁面       | API 路徑                         | 篩選參數範例                        |
|------------|----------------------------------|-------------------------------------|
| candidates | `/admin/api/products`           | `?item_status=candidate`            |
| products   | `/admin/api/products`           | `?item_status=selected`             |
| stocks     | `/admin/api/products`           | `?item_status=selected&with_stock=true` |
| account    | `/admin/api/account/...`        | 自定義                              |

---

## 🧩 欄位設定與卡片渲染方式

每個 page 的 JS 控制器可定義欄位列表：

```js
const field_config = ["stall_name", "id", "name", "status", "images"];
```

該設定傳入 `card_renderer.js`，統一渲染 DOM。

---

## 🔧 維護策略重點

- 所有資料頁使用共用 API，避免重複查詢邏輯
- HTML 使用模板繼承，維護簡單
- 欄位與 DOM 拆分渲染，易於調整欄位順序或新增欄位
- 未來擴充如 drafts/reports 只需調整 route 與 config

---

## 📝 TODO 建議

- [ ] 四頁頁面 + route + template 搭建
- [ ] 每頁主控 JS 接通
- [ ] 欄位設定抽離為常數或 JSON
- [ ] 加入批次選取 / 狀態編輯功能
- [ ] 加入帳號驗證、權限管理
