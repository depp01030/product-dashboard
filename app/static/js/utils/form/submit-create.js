// 📁 static/js/utils/form/submit-create.js
import { extractFormData } from "./form-submit.js";
import { renderProductCard } from "../dom/render-card.js";

/**
 * 提交 temp 表單並使用建立成功的商品資料替換卡片
 */
export async function submitCreateHandler(e, form) {
  e.preventDefault();
  const formData = extractFormData(form, false);

  const res = await fetch("/admin/products/create", {
    method: "POST",
    body: formData
  });
  if (res.ok) {
    const newProduct = await res.json();
    console.log("newProduct", newProduct);
    const card = renderProductCard(newProduct, {
      showFields: form.dataset.showFields.split(","),
      submitPath: "/admin/products",
      renderAsCheckbox: form.dataset.renderAsCheckbox === "true"
    });
    const wrapper = form.closest(".col-12");
    wrapper.replaceWith(card);
  } else {
    const button = form.querySelector("button[type=submit]");
    button.className = "btn btn-danger btn-sm px-3";
    button.innerHTML = `<i class="bi bi-x-lg"></i> 建立失敗`;
    setTimeout(() => {
      button.className = "btn btn-primary btn-sm px-3";
      button.innerHTML = "儲存";
    }, 1800);
  }
}
