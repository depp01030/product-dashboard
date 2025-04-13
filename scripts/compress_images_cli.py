import os
import sys
import shutil

# 加入專案路徑
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.utils.config import get_candidates_root

def clean_compressed_images(root_dir: str) -> tuple[int, int]:
    """
    清理所有壓縮圖片：
    1. 刪除所有 thumbs 資料夾
    2. 刪除所有檔名中包含 compressed 的圖片
    Returns: tuple[int, int] - (已刪除的 thumbs 資料夾數量, 已刪除的壓縮圖片數量)
    """
    thumbs_count = 0
    compressed_files_count = 0
    
    for root, dirs, files in os.walk(root_dir):
        # 1. 刪除 thumbs 資料夾
        if "thumbs" in dirs:
            thumbs_path = os.path.join(root, "thumbs")
            try:
                shutil.rmtree(thumbs_path)
                thumbs_count += 1
                print(f"已刪除資料夾: {thumbs_path}")
            except Exception as e:
                print(f"刪除資料夾失敗 {thumbs_path}: {e}")

        # 2. 刪除包含 compressed 的圖片檔案
        for file in files:
            if "compressed" in file.lower() and file.lower().endswith(('.jpg', '.jpeg', '.png')):
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    compressed_files_count += 1
                    print(f"已刪除檔案: {file_path}")
                except Exception as e:
                    print(f"刪除檔案失敗 {file_path}: {e}")
    
    return thumbs_count, compressed_files_count

if __name__ == "__main__":
    candidates_root = get_candidates_root()
    print(f"開始清理壓縮圖片...")
    thumbs_count, files_count = clean_compressed_images(candidates_root)
    print(f"✅ 清理完成:")
    print(f"  - 已刪除 {thumbs_count} 個 thumbs 資料夾")
    print(f"  - 已刪除 {files_count} 個包含 compressed 的圖片檔案")