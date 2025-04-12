# ShopeeAPI 架構說明與 MVC 對應

本系統採用 FastAPI 為主架構，結合現代 Web API 設計原則，模組分工清楚、易於維護與擴展。以下為各模組功能與其對應 MVC 架構角色。

---

## 📦 資料夾結構總覽

ShopeeAPI/
├── main.py                  # FastAPI 應用啟動點（uvicorn main:app）
├── .env                     # 資料庫連線資訊
├── requirements.txt
├── app/
│   ├── api/                 # ✅ 負責定義 API 路由，串接 service（= controller）
│   │   └── item_routes.py   # /items 相關 endpoints（CRUD）
│   ├── schemas/             # ✅ 定義資料傳輸格式（DTO）：驗證、序列化
│   │   └── item.py
│   ├── models/              # ✅ 定義資料表結構（對應 DB 的 table，ORM）
│   │   └── item.py
│   ├── services/            # ✅ 業務邏輯與資料處理（可理解為簡化版 DAO + Service Layer）
│   │   └── item_service.py
│   └── utils/               # 工具類（DB 初始化、載入 config、logger 等）
│       ├── config.py
│       └── db.py


---

## 🧠 MVC 對應角色說明

| FastAPI 模組          | MVC 對應角色     | 功能說明 |
|----------------------|------------------|----------|
| `app/models/*.py`     | **Model**         | 資料表定義，使用 SQLAlchemy ORM 對應 MySQL |
| `app/schemas/*.py`    | **DTO / 表單驗證** | 使用 Pydantic 定義 request/response 結構，處理資料驗證與序列化 |
| `app/services/*.py`   | **Service / DAO** | 處理資料邏輯與 ORM 操作，封裝為可重用邏輯 |
| `app/api/*.py`        | **Controller**    | 定義 API 路由與請求處理流程，調用 services |
| `main.py`             | **啟動點**        | 建立 app 實例、掛載 router、初始化環境與資料庫 |
| `/docs` (Swagger UI) | **View**          | 提供 API 操作介面給前端或測試使用者 |
| `app/utils/*.py`      | **基礎工具**      | 處理設定讀取、DB engine 建立、Session 管理等基礎架構層功能 |

---

## 🔁 一次請求流程（範例：建立一筆商品）

1. Client 呼叫 POST `/items/`，送出 JSON 資料
2. `api/item_routes.py` 解析路由 → 檢查資料（使用 `ItemCreate` schema）
3. 呼叫 `services/item_service.py` 執行資料處理邏輯
4. 使用 `models/item.py` 建立 ORM 實例並寫入資料庫
5. 回傳結果 → 再轉換為 `ItemInDB` schema → 傳回給 Client
6. Swagger UI 顯示完整結果

---

## ✅ 設計優勢

- 模組分離：每層只負責單一職責
- 容易擴展：新增模組不需改動其他邏輯
- 測試友善：Service 層可單獨測試邏輯，Schema 層自帶驗證
- 文件清楚：Swagger UI 自動生成 API 文件

---

## 🔚 附註

此架構風格為 MVC 模式的現代實踐，結合 DTO 與 Service Layer，適合中大型系統使用，且方便日後導入 RESTful API、OpenAPI、OAuth 認證、RBAC 權限等。

