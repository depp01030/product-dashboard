# 📦 環境變數與設定管理指南

## ✅ 我們遵循的 5 大原則

1. **開發預設值寫在 `settings.py`，部署用環境變數覆蓋**
    - ✅ 好處是讓使用者 fork 或 clone 下來，不用 .env 就能直接啟動（因為有預設值）
2. **敏感資訊（如密碼、金鑰）寫在 .env，並加入 .gitignore** 
    - ✅ `.env` 檔案不應該被 commit，應該加入 `.gitignore`
    - ✅ 敏感資訊應該由 Docker、CI/CD 或雲平台注入，而不是寫死在程式碼中
3. **敏感資訊（.env) 應由 Docker、CI/CD 或雲平台注入**
    - ✅ 應由部署流程顯式設定變數，例如 -e APP_ENV=production>
4. **不推薦 `.env` 判斷執行環境，請用明確用注入`IS_DOCKER`** 
    - ✅ 把環境狀態的主導權交給部署方式，而非檔案本身
    - ✅ 例如：`docker run -e IS_DOCKER=true` 或 CI/CD 平台的 Secrets
5. **提供 `.env.example` 供開發者參考**
    - ✅ 讓開發者知道怎麼建立自己的 .env

---

## 2️⃣ 三層結構：設定檔與環境變數的分工

| 名稱       | 負責內容                                | 是否進入版本控制 | 來源             |
|------------|------------------------------------------|------------------|------------------|
| `.env`     | 存放敏感資訊與開發環境變數（文字檔）              | 否               | 檔案手動建立或 CI 注入 |
| `settings.py` | 由 `BaseSettings` 管理設定邏輯與預設值        | ✅               | 程式定義 + `.env`/環境變數 |
| `config.py`   | 根據 `settings` 組合邏輯值（如路徑、URL）       | ✅               | 程式內部邏輯組合   |

---

## 🧱 設計範本

### `.env`（實際使用，不commit）

```dotenv
APP_BASE_URL=http://localhost:8000
DB_USER=admin
DB_PASSWORD=s3cr3t
SECRET_KEY=mykey
IS_DOCKER=false
```

> 🔐 請勿將 `.env` 加入版本控制，避免敏感資訊外洩。
---

### `.env.example`（供團隊參考）

```dotenv
APP_BASE_URL=
DB_USER=
DB_PASSWORD=
SECRET_KEY=
IS_DOCKER=
```

> 📌 說明：此檔案提供開發人員參考，實際使用時請複製為 `.env` 並填入對應值。
---

### `settings.py`

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_base_url: str = "http://localhost:8000"
    db_user: str = "root"
    db_password: str
    secret_key: str
    is_docker: bool = False

    model_config = {
        "env_file": ".env",      # 開發用 .env
        "extra": "allow"         # 避免多餘變數報錯
    }

settings = Settings()
```

---

### `config.py`

```python
from settings import settings

# 動態組合圖片網址邏輯
def get_image_base_url():
    if settings.is_docker:
        return "https://cdn.example.com/images"
    return f"{settings.app_base_url}/images"
```

---

## 🌐 不同環境的變數處理

| 環境         | 推薦做法                                         |
|--------------|--------------------------------------------------|
| 本地開發       | `.env` + `settings.py` 預設值                        |
| Docker 部署   | `docker run -e VAR=...` 或 `docker-compose.yml` 配置 |
| CI/CD         | 在平台設定 Secrets 或環境變數                           |
| 雲平台（如 Heroku、Vercel） | 在 Web 管理介面設定環境變數                      |

---

## 🚫 不推薦的做法

- ❌ 把密碼、金鑰直接寫進程式碼中
- ❌ 用 `.env` 判斷環境狀態（如 `IS_PRODUCTION=true`），而不讓部署環境決定
- ❌ commit `.env` 到版本控制（記得 `.gitignore`）

---

## 🧩 常見陷阱

| 問題                            | 解法                                   |
|----------------------------------|----------------------------------------|
| 啟動報錯：missing settings       | 檢查 `.env` 是否提供，或給 `settings` 預設值 |
| 布林值錯誤（"true" ≠ True）     | 使用 `bool` 型別 + `.env` 寫 `true/false` |
| 預設寫死生產環境設定            | 只在 `.env` 提供生產值，不要寫死在程式碼中 |

---

## 🧪 測試建議

- 使用 `print(settings.dict())` 驗證設定有無正確注入
- 用 `pytest` + `monkeypatch` 模擬環境變數覆蓋測試
- 建議新增 `test_env.py` 測試設定載入行為是否正確

---

## ✅ 總結

> ✨ **預設是為開發設計的，部署由環境變數負責控制**  
> 🔐 **機密永遠不要 commit，設定永遠要清楚切分**

```
