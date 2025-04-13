import enum

class ItemStatusEnum(str, enum.Enum):
    candidate = "candidate"
    product = "product"
    ignore = "ignore"

class LogisticsOptionEnum(str, enum.Enum):
    seven_eleven = "7-ELEVEN"
    familymart = "全家"
    hilife = "萊爾富"
    shopee_store_pickup = "蝦皮店到店"

class CustomTypeEnum(str, enum.Enum):
    top = "女性上著"
    bottom = "女性下著"
    dress = "洋裝"
    coat = "外套"
    skirt = "裙子"
    pants = "褲子"
    accessories = "配飾"
    scarf = "圍巾"
    other = "其他"

class SizeMetricsEnum(str, enum.Enum):
    shoulder = "肩寬"
    bust = "胸圍"
    waist = "腰圍"
    hip = "臀圍"
    length = "衣長"
    sleeve = "袖長"
    inseam = "內檔長"
