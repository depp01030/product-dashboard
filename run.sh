#!/bin/bash

set -e

CONTAINER_NAME="hers-backend"
IMAGE_NAME="hers-backend"
HOST_PORT=8000
CONTAINER_PORT=8000
ENV_FILE=".env"
HOST_PRODUCTS_PATH="/Applications/Depp/products_root"
CONTAINER_PRODUCTS_PATH="/app/images"

echo "🧹 嘗試移除舊容器（如果存在）..."
docker rm -f $CONTAINER_NAME 2>/dev/null || true

echo "🚀 啟動新的容器 $CONTAINER_NAME"
docker run -d \
  --name $CONTAINER_NAME \
  -p ${HOST_PORT}:${CONTAINER_PORT} \
  --env-file $ENV_FILE \
  -v ${HOST_PRODUCTS_PATH}:${CONTAINER_PRODUCTS_PATH} \
  $IMAGE_NAME

echo "✅ 容器已啟動 → http://localhost:$HOST_PORT/docs"
