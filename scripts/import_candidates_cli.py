# scripts/import_candidates_cli.py

import os
import sys

# 加入專案路徑讓 Python 找到 app 模組
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.import_service import import_candidates_from_folder

if __name__ == "__main__":
    count = import_candidates_from_folder()
    print(f"✅ 成功匯入 {count} 筆候選款式")
