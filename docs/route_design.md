# 📚 Shopee 自動上架後台系統 API Routes

## 🛒 商品管理（文字資料）

| 功能 | 路由 | 方法 | 說明 |
| :--- | :--- | :--- | :--- |
| 查詢商品列表 | `/api/admin/products` | `GET` | 支援分頁、篩選、排序 |
| 新增商品（純文字資料） | `/api/admin/products` | `POST` | 送 JSON（不含圖片） |
| 查詢單一商品詳情 | `/api/admin/products/{product_id}` | `GET` | 查詢某個商品的完整資料 |
| 更新商品資料（純文字） | `/api/admin/products/{product_id}` | `PUT` | 更新商品文字欄位 |
| 刪除單一商品 | `/api/admin/products/{product_id}` | `DELETE` | 刪除指定商品 |
| 批次刪除商品 | `/api/admin/products/batch-delete` | `POST` | 一次刪除多個商品，傳 id 陣列 |

---

## 🖼️ 商品圖片管理（圖片上傳/刪除）

| 功能 | 路由 | 方法 | 說明 |
| :--- | :--- | :--- | :--- |
| 上傳商品圖片 | `/api/admin/products/{product_id}/images` | `POST` | 上傳主圖、附圖（FormData） |
| 查詢商品圖片清單 | `/api/admin/products/{product_id}/images` | `GET` | 回傳所有圖片清單（可標記主圖） |
| 刪除單張圖片 | `/api/admin/products/{product_id}/images/{filename}` | `DELETE` | 刪除特定圖片 |

---

## 🔒 登入系統（認證管理）

| 功能 | 路由 | 方法 | 說明 |
| :--- | :--- | :--- | :--- |
| 登入 | `/api/admin/auth/login` | `POST` | 提交帳號密碼，登入取得 token |
| 登出 | `/api/admin/auth/logout` | `POST` | 登出，清除登入狀態 |
| 取得目前使用者資訊 | `/api/admin/auth/me` | `GET` | 查詢目前登入的使用者資訊 |

---

# ✨ 說明

- 商品基本資料（名稱、價格、描述等）與圖片（主圖/附圖）分開兩段提交。
- 文字資料走 `application/json`
- 圖片上傳走 `multipart/form-data`
- 後端依據 Content-Type 正確解析
- 成功建商品後會回傳 `product_id`，前端再根據這個 id 上傳圖片。
