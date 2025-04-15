// 📁 static/js/utils/form/form-submit.js
import { extractDynamicListValues, extractDynamicKVValues } from "../dom/product-card-widget.js";

const SIZE_METRICS_BY_TYPE = {
  top: ["shoulder", "bust", "length", "sleeve"],
  bottom: ["waist", "hip", "length", "inseam"],
  dress: ["shoulder", "bust", "waist", "length"],
  coat: ["shoulder", "bust", "length", "sleeve"],
  skirt: ["waist", "hip", "length"],
  pants: ["waist", "hip", "length", "inseam"],
  accessories: [],
  scarf: ["length"],
  other: []
};

export function extractFormData(form, renderAsCheckbox = false) {
  const formData = new FormData(form);

  // 圖片選擇
  const selectedImages = Array.from(
    form.querySelectorAll(".image-checkbox:checked")
  ).map(cb => cb.value);
  formData.set("selected_images", selectedImages.join(","));

  // 主圖
  const mainImage = formData.get("main_image") || "";
  formData.set("main_image", mainImage);

  // 類別
  const customType = formData.get("custom_type") || ""; 
  formData.set("custom_type", customType);

  // 顏色
  const colorListContainer = form.querySelector("#colors-widget");
  if (colorListContainer) {
    const colors = extractDynamicListValues(colorListContainer);
    formData.set("colors", colors.join(","));
  }

  // 尺寸（選項）
  const sizeListContainer = form.querySelector("#sizes-widget");
  if (sizeListContainer) {
    const sizes = extractDynamicListValues(sizeListContainer);
    formData.set("sizes", sizes.join(","));
  }

  // 尺寸明細
  const kvContainer = form.querySelector("#size-metrics-widget");
  if (kvContainer) {
    const keys = kvContainer.querySelectorAll("input[name$='_key[]']");
    const values = kvContainer.querySelectorAll("input[name$='_value[]']");
    const result = {};

    for (let i = 0; i < keys.length; i++) {
      const k = keys[i].value.trim();
      const v = values[i].value.trim();

      if (!k && v) {
        alert("尺寸明細中有數值但未填欄位名稱，請補上欄位名稱！");
        throw new Error("無效尺寸欄位：key 為空但有值");
      }

      if (k) result[k] = v;
    }

    formData.set("size_metrics", JSON.stringify(result)); 
  }

  return formData;
}

export async function submitProductForm(e, form, renderAsCheckbox = false) {
  e.preventDefault();
  const formData = extractFormData(form, renderAsCheckbox);
  const button = form.querySelector("button[type=submit]");
  if (button) {
    button.disabled = true;
    button.innerHTML = `<span class="spinner-border spinner-border-sm me-1"></span> 儲存中...`;
  }

  const res = await fetch(form.action, {
    method: "POST",
    body: formData
  });

  if (button) {
    if (res.ok) {
      button.className = "btn btn-success btn-sm px-3";
      button.innerHTML = `<i class="bi bi-check2"></i> 已儲存`;
    } else {
      button.className = "btn btn-danger btn-sm px-3";
      button.innerHTML = `<i class="bi bi-x-lg"></i> 儲存失敗`;
    }

    setTimeout(() => {
      button.className = "btn btn-primary btn-sm px-3";
      button.innerHTML = "儲存";
      button.disabled = false;
    }, 1800);
  }
}
