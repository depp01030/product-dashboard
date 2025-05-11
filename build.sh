#!/bin/bash

set -e  # 發生錯誤就終止

echo "🔨 建立 Docker 映像檔：hers-backend"
docker build -t hers-backend .

echo "✅ Build 成功"
