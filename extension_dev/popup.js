document.getElementById("product-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const form = e.target;
    const msg = document.getElementById("status-msg");
  
    const formData = new FormData(form);
    const data = {};
  
    for (const [key, value] of formData.entries()) {
      if (["price", "real_stock", "shopee_category_id", "min_purchase_qty", "preparation_days"].includes(key)) {
        data[key] = value ? Number(value) : null;
      } else if (["colors", "sizes", "logistics_options"].includes(key)) {
        data[key] = value ? value.split(",").map(s => s.trim()).filter(s => s) : [];
      } else if (key === "size_metrics") {
        try {
          data[key] = value ? JSON.parse(value) : {};
        } catch (err) {
          showError(`尺寸資料 (size_metrics) 不是正確的 JSON`);
          return;
        }
      } else {
        data[key] = value || null;
      }
    }
  
    try {
      const res = await fetch("http://localhost:8000/products/create", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      });
  
      const contentType = res.headers.get("Content-Type") || "";
      const isJson = contentType.includes("application/json");
  
      if (res.ok) {
        msg.textContent = "✅ 已成功送出！";
        msg.className = "text-success text-center mt-2 small";
        form.reset();
      } else if (isJson) {
        const json = await res.json();
        showError(json.detail || "❌ 發生錯誤，請檢查欄位格式");
      } else {
        const text = await res.text();
        showError(`❌ 錯誤回應：${text}`);
      }
    } catch (err) {
      showError(`🚫 無法連線到伺服器：${err.message}`);
    }
  
    function showError(message) {
      msg.textContent = message;
      msg.className = "text-danger text-center mt-2 small";
    }
  });
  