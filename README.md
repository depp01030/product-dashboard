# Shopee 自動化上架系統

## 一、專案目標
建立一套可擴展的自動上架服務，透過 Excel 輸入商品資料、自動整理上傳至 Shopee 平台，並預留未來擴展至 Web 後台管理系統與多主機部署能力。

---

## 二、系統架構與文件目錄

```bash
shopee_uploader/
├── app/                            # 專案核心部分
│   ├── __init__.py
│   ├── models/                     # SQLAlchemy 資料模型
│   │   ├── __init__.py
│   │   ├── item.py
│   │   ├── item_image.py
│   │   └── listing_log.py
│   ├── services/                   # 各種業務流程 (Service Layer)
│   │   ├── __init__.py
│   │   ├── excel_importer.py       # Excel 輸入流程
│   │   ├── item_uploader.py        # 上架 Shopee 處理
│   │   └── gpt_reviewer.py         # GPT 審查模組（未來）
│   ├── api/                        # Web API endpoints (Flask routes)
│   │   ├── __init__.py
│   │   ├── item_routes.py
│   │   └── health_check.py
│   ├── utils/                      # 工具 & 共用程式碼
│   │   ├── __init__.py
│   │   ├── db.py                   # DB 設定與 Session 管理
│   │   ├── config.py               # 設定讀取 (.env)
│   │   └── logger.py               # 日誌設定
│   └── main.py                     # Flask 啟動進入點
├── migrations/                     # DB Migration（選用 Alembic）
├── static/                         # 圖片 / 靜態資料
├── templates/                      # Web 前端模板
├── .env                            # 環境變數 (.env 設定)
├── requirements.txt
├── README.md
├── run.py                          # local dev 啟動檔（選用）
└── docs/
    └── architecture.md             # 系統設計筆記
```

---

## 三、設計原則

- 設計基於 **模組化與易於維護**
- 使用 **Service Layer** 分離商業邏輯
- 使用 **Flask Blueprint** 拆分 API route
- 資料庫操作使用 **SQLAlchemy ORM**
- 預留 **GPT 輔助審查模組**
- 預留圖像管理模組（S3 / CDN）
- 支援 .env 管理敏感資訊
- 同步多主機環境與部署對應

---

## 四、技術選型

| 技術 | 用途 |
|--------|------|
| Python 3.9.21 | 主程式語言 |
| Flask | Web API / 後台管理系統 |
| SQLAlchemy | ORM 表示與操作 DB |
| pandas + openpyxl | Excel 資料讀取與轉換 |
| requests | Shopee API 操作 |
| Pillow + boto3 | 圖片處理 + 物件儲存 |
| openai | GPT-4o 輔助表單審查 |

---

## 五、使用指引 (Getting Started)

```bash
# 建立 virtualenv
python3 -m venv venv
source venv/bin/activate

# 安裝相關套件
pip install -r requirements.txt

# 設定 .env 環境變數 (MySQL info)

# 執行主程式
python app/main.py
```

詳細系統設計請見 [docs/architecture.md](docs/architecture.md)