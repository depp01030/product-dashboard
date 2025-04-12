# ShopeeAPI 命名規則指南

本命名規則參考 Python 社群慣例（PEP8）與 MVC 實作邏輯，適用於本專案的 FastAPI 架構。

---

## 📁 資料夾命名（snake_case）

| 資料夾         | 說明                            |
|----------------|---------------------------------|
| `models/`      | 定義 ORM 資料表模型             |
| `schemas/`     | 定義資料驗證與輸出格式（Pydantic） |
| `services/`    | 封裝商業邏輯、資料操作          |
| `api/`         | 定義 HTTP 路由與 API            |
| `utils/`       | 共用功能（DB 初始化、config 等） |

---

## 📄 檔案命名（snake_case）

| 類型        | 檔名範例           | 說明                         |
|-------------|--------------------|------------------------------|
| ORM 模型    | `item.py`          | 對應一張表格，檔案名用單數   |
| Schema      | `item.py`          | 和 model 同名，放不同資料夾 |
| Service     | `item_service.py`  | 模型 + `_service` 命名方式  |
| API Router  | `item_routes.py`   | 模型 + `_routes` 命名方式   |
| 公用工具    | `db.py`, `config.py` | 描述功能用途即可             |

---

## 🧱 類別命名（PascalCase）

| 類別         | 命名範例                     | 說明                               |
|--------------|------------------------------|------------------------------------|
| ORM Model    | `Item`                       | 對應 DB 資料表（單數）             |
| Schema       | `ItemCreate`, `ItemUpdate`, `ItemInDB` | 用於新增、更新、回傳格式         |
| 自定義錯誤   | `ItemNotFoundError`          | 明確標示錯誤用途                   |

---

## 🔧 函式命名（snake_case）

| 類型         | 命名範例                         | 說明                                   |
|--------------|----------------------------------|----------------------------------------|
| Service 函式 | `create_item()`, `get_item()`    | 操作資料表，動詞開頭                   |
| Route 函式   | `create()`, `read_one()`         | API handler，語意簡潔 RESTful          |
| 工具函式     | `get_database_uri()`, `load_env()` | 獨立功能性操作                         |

---

## 📌 REST API 路由命名（小寫複數）

| 路由             | 方法     | 說明         |
|------------------|----------|--------------|
| `/items/`        | `GET`    | 取得所有商品 |
| `/items/{id}`    | `GET`    | 查詢單一商品 |
| `/items/`        | `POST`   | 新增商品     |
| `/items/{id}`    | `PUT`    | 更新商品     |
| `/items/{id}`    | `DELETE` | 刪除商品     |

---

## ✅ 命名風格總表

| 分類     | 檔名                | class/function 命名建議                      |
|----------|---------------------|----------------------------------------------|
| Model    | `item.py`           | `Item`（首字大寫）                           |
| Schema   | `item.py`           | `ItemCreate`, `ItemUpdate`, `ItemInDB`       |
| Service  | `item_service.py`   | `create_item`, `get_item`, `update_item`... |
| API      | `item_routes.py`    | `@router.post("/items/")` 對應 CRUD         |
| Tool     | `config.py`, `db.py`| `get_database_uri()`, `Base`, `engine`       |

---

## 🔚 附註

- 所有命名遵循「語意清楚 + 一致性優先」原則
- Schema 命名應明確表示用途：Create / Update / InDB / Out 等
- Router 與 Service 命名應配對，方便追蹤功能鏈路
