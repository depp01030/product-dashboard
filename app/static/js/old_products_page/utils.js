// static/js/utils.js

// ✅ 將字串轉小寫，避免 null 錯誤
export function toSafeLower(str) {
    return (str || '').toLowerCase();
}

// ✅ 支援通配符 * 模式的模糊比對（例如 *粉*色*）
export function matchKeywordWildcard(target, keyword) {
    if (!keyword) return true;
    const safeTarget = toSafeLower(target);
    const parts = keyword.toLowerCase().split('*').filter(Boolean);
    return parts.every(part => safeTarget.includes(part));
}

// ✅ 將 JS Date 格式化為 YYYY-MM-DD 字串
export function formatDate(date) {
    const yyyy = date.getFullYear();
    const mm = String(date.getMonth() + 1).padStart(2, '0');
    const dd = String(date.getDate()).padStart(2, '0');
    return `${yyyy}-${mm}-${dd}`;
}
