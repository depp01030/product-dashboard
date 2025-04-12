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
    top = "女用上著"
    bottom = "女用下著"
    scarf = "圍巾"
    other = "其他"
