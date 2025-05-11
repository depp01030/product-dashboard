# 第一階段：使用輕量 Python 基底映像
FROM python:3.10-slim

# 設定工作目錄
WORKDIR /app

# 複製 requirements 並安裝
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製整個專案到容器
COPY . .

# 若你使用 .env，可以在這裡自訂
# 取消 Python 的緩衝區，讓日誌即時輸出
ENV PYTHONUNBUFFERED=1  

# 預設啟動指令：FastAPI 入口是 main.py，app 物件在 main.py 裡
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
