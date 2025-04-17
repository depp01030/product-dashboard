// static/js/utils/form/form-submit.js
import { extractDynamicListValues, extractDynamicKVValues } from "../dom/product-card-widget.js";

const NUM_FIELDS = ["purchase_price","total_cost","price"];

export function extractFormData(form){
  const fd = new FormData(form);

  /* ---------- 刪掉空 numeric 欄位 ---------- */
  NUM_FIELDS.forEach(k=>{ if(fd.get(k)==="") fd.delete(k); });

  /* ---------- selected_images (append) ---------- */
  // 1. 先把舊的全部刪掉
  fd.delete("selected_images[]"); // 先移除可能殘留的舊值

  // 2. 對「舊圖但有打勾」的每一張 append
  form.querySelectorAll(".image-checkbox:checked")
      .forEach(cb => fd.append("selected_images[]", cb.value));

  // 3. 對「臨時圖且有打勾」的每一張 append
  form.querySelectorAll(".temp-checkbox")
      .forEach(cb => {
        if (cb.checked) {
          const filename = cb.closest(".card")
                            .querySelector("img")
                            .src.split("/").pop();   // 取檔名
          fd.append("selected_images[]", filename);
        }
      });

  /* ---------- dynamic widgets ---------- */
  const colorBox = form.querySelector("#colors-widget");
  if(colorBox) fd.set("colors", extractDynamicListValues(colorBox).join(","));
  const sizeBox = form.querySelector("#sizes-widget");
  if(sizeBox) fd.set("sizes", extractDynamicListValues(sizeBox).join(","));
  const kvBox = form.querySelector("#size-metrics-widget");
  if(kvBox)   fd.set("size_metrics", JSON.stringify(extractDynamicKVValues(kvBox)));

  /* ---------- append all imported files ---------- */
  form.querySelectorAll(".image-module").forEach(mod=>{
    if(Array.isArray(mod.tempFiles)) mod.tempFiles.forEach(f=>fd.append("image_import",f));
  });

  return fd;
}

export async function submitProductForm(e,form){
  e.preventDefault();
  const fd = extractFormData(form);
  const btn = form.querySelector("button[type=submit]");
  if(btn){btn.disabled=true;btn.innerHTML="<span class='spinner-border spinner-border-sm me-1'></span> 儲存中...";}
  const res = await fetch(form.action,{method:"POST",body:fd});
  if(btn){
    btn.className = res.ok?"btn btn-success btn-sm px-3":"btn btn-danger btn-sm px-3";
    btn.innerHTML = res.ok?"<i class='bi bi-check2'></i> 已儲存":"<i class='bi bi-x-lg'></i> 儲存失敗";
    setTimeout(()=>{btn.className="btn btn-primary btn-sm px-3";btn.innerHTML="儲存";btn.disabled=false;},1800);
  }
}
