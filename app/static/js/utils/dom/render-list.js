// 📁 static/js/utils/render-list.js

let totalCount = 0;

/**
 * 清空商品列表
 */
export function clearList(container) {
  container.innerHTML = "";
  totalCount = 0;
  updateItemCount();
}

/**
 * 插入卡片到列表中，每張卡片占據整行
 */
export function appendToList(container, card) {
  const wrapper = document.createElement("div");
  wrapper.className = "col-12 mb-4"; // 改為 col-12 讓卡片占據整行
  wrapper.appendChild(card);
  container.appendChild(wrapper);
  totalCount += 1;
  updateItemCount();
}

/**
 * 更新畫面上的商品筆數統計
 */
export function updateItemCount() {
  const counter = document.getElementById("item-count");
  if (counter) {
    counter.textContent = `目前共 ${totalCount} 筆`;
  }
}
