// static/js/item_status_options.js

/**
 * ✅ 產生商品狀態選單的 <option> HTML 字串
 * @param {string} selected - 當前選中的狀態（例如：'candidate'）
 * @returns {string} HTML <option> 組合
 */
export function generateItemStatusOptions(selected = "") {
    const options = {
      candidate: "待選商品",
      product: "已選商品",
      ignore: "忽略",
    };
  
    return Object.entries(options)
      .map(([value, label]) =>
        `<option value="${value}" ${selected === value ? "selected" : ""}>${label}</option>`
      )
      .join("\n");
  }
  