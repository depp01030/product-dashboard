// 📁 static/js/utils/pagination.js

let offset = 0;

/**
 * 重設 offset
 */
export function resetPagination() {
  offset = 0;
}

/**
 * 取得目前 offset
 */
export function getCurrentOffset() {
  return offset;
}

/**
 * 增加 offset
 */
export function increaseOffset(by = 20) {
  offset += by;
}

/**
 * 判斷是否顯示載入更多按鈕
 */
export function shouldShowLoadMore(receivedCount, pageSize) {
  return receivedCount >= pageSize;
}

/**
 * 綁定載入更多按鈕事件
 */
export function bindLoadMore(button, callback) {
  if (!button) return;
  button.addEventListener("click", () => {
    callback();
  });
}