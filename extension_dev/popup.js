// ✅ 暫存輸入值（打開/關掉仍保留）
// ✅ 自動轉型與錯誤提示

const form = document.getElementById("product-form");
const msg = document.getElementById("status-msg");

// === 初始化欄位 ===
window.addEventListener("DOMContentLoaded", () => {
  for (const el of form.elements) {
    if (el.name) {
      chrome.storage.local.get(el.name, (result) => {
        if (result[el.name]) el.value = result[el.name];
      });
    }
  }
});

// === 輸入即時儲存 ===
form.addEventListener("input", (e) => {
  if (e.target.name) {
    chrome.storage.local.set({ [e.target.name]: e.target.value });
  }
});

// === 表單送出 ===
form.addEventListener("submit", async (e) => {
  e.preventDefault();
  msg.textContent = "⏳ 送出中...";
  msg.className = "text-muted text-center small";

  const data = {};
  for (const el of form.elements) {
    if (!el.name) continue;
    const value = el.value.trim();

    if (["price", "real_stock"].includes(el.name)) {
      data[el.name] = value ? Number(value) : null;
    } else if (["colors", "sizes"].includes(el.name)) {
      data[el.name] = value ? value.split(",").map(s => s.trim()) : [];
    } else {
      data[el.name] = value || null;
    }
  }

  try {
    const res = await fetch("http://localhost:8000/admin/products/create", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });

    if (res.ok) {
      msg.textContent = "✅ 成功送出！";
      msg.className = "text-success text-center small";
      form.reset();
      chrome.storage.local.clear();
    } else {
      const err = await res.json();
      msg.textContent = "❌ 錯誤：" + (err.detail || "無法解析錯誤");
      msg.className = "text-danger text-center small";
    }
  } catch (err) {
    msg.textContent = "🚫 無法連線：" + err.message;
    msg.className = "text-danger text-center small";
  }
});
