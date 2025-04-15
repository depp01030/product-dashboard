// 📁 static/js/utils/data/metrics.js

/**
 * 對應每一種商品類別（custom_type）所需的尺寸欄位（size_metrics）
 */
export const SIZE_METRICS_BY_TYPE = {
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
  
  /**
   * 每一種尺寸欄位的中文標籤
   */
  export const SIZE_METRIC_LABELS = {
    shoulder: "肩寬",
    bust: "胸圍",
    waist: "腰圍",
    hip: "臀圍",
    length: "衣長",
    sleeve: "袖長",
    inseam: "內檔長"
  };
  
  /**
   * custom_type 的中文名稱，用於選單顯示
   */
  export const CUSTOM_TYPE_OPTIONS = {
    top: "女性上著",
    bottom: "女性下著",
    dress: "洋裝",
    coat: "外套",
    skirt: "裙子",
    pants: "褲子",
    accessories: "配飾",
    scarf: "圍巾",
    other: "其他"
  };
  