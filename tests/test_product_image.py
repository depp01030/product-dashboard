# 📁 tests/test_product_image.py

import io
import json
import sys
import os
from fastapi.testclient import TestClient

sys.path.append(os.path.abspath("."))  # 加入專案根目錄

from main import app
print("Using TestClient from:", TestClient.__module__)
print("***************app type is:", type(app))

client = TestClient(app)

def test_process_product_images():
    
    fake_image = io.BytesIO(b"fake image content")
    fake_image.seek(0)

    images = [
        {
            "tempId": "abc123",
            "action": "new",
            "isMain": True,
            "isSelected": True,
        }
    ]

    data = {
        "images": json.dumps(images)
    }

    files = {
        "file_abc123": ("test.jpg", fake_image, "image/jpeg")
    }

    response = client.post("/api/admin/product-images/123/process", data=data, files=files)

    assert response.status_code == 200, response.text
    result = response.json()
    assert isinstance(result, list)
    assert result[0]["filename"].endswith(".jpg")
    assert result[0]["product_id"] == 123
