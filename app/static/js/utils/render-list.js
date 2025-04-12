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
 * 插入卡片到列表中，使用 Bootstrap row + col-md-6 排版
 */
export function appendToList(container, card) {
  const wrapper = document.createElement("div");
  wrapper.className = "col-md-6 mb-4";
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
