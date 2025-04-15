// 📁 static/js/utils/item-operation.js
import { renderProductCard } from "./dom/render-card.js";
import { updateItemCount } from "./dom/render-list.js";
import { submitCreateHandler } from "./form/submit-create.js";

/**
 * 新增一張暫時商品卡片，放在最上方
 * 成功送出後將會以正式商品資料替換
 */
export function addtempItemCard(container, showFields = [], submitPath = "/admin/products") {
  const tempProduct = {
    id: "temp_" + Date.now(),
    image_dir: "",
    image_list: [],
    selected_images: [],
    main_image: "",
    custom_type: "",
    size_metrics: {},
    item_status: "product"
  };

  const card = renderProductCard(tempProduct, {
    showFields,
    submitPath,
    renderAsCheckbox: false,
    onSubmit: submitCreateHandler
  });

  // 暫存參數附加到 DOM 上，讓 handler 可讀取
  card.dataset.showFields = showFields.join(",");
  card.dataset.renderAsCheckbox = "false";

  const wrapper = document.createElement("div");
  wrapper.className = "col-12 mb-4";
  wrapper.appendChild(card);
  container.insertBefore(wrapper, container.firstChild);

  updateItemCount();
}
