import enum

class ItemStatusEnum(str, enum.Enum):
    product = "product"

class LogisticsOptionEnum(str, enum.Enum):
    seven_eleven = "seven_eleven" #"7-ELEVEN"
    familymart = "familymart" #"全家"
    hilife = "hilife" #"萊爾富"
    shopee_store_pickup = "shopee_store_pickup" #"蝦皮店到店"

class CustomTypeEnum(str, enum.Enum):
    top = "top"        # "女性上著"
    bottom = "bottom"  # "女性下著"
    dress = "dress"    # "洋裝"
    coat = "coat"      # "外套"
    skirt = "skirt"    # "裙子"
    pants = "pants"    # "褲子"
    accessories = "accessories" # "配飾"
    scarf = "scarf"    # "圍巾"
    other = "other"    # "其他"

class SizeMetricsEnum(str, enum.Enum):
    shoulder = "shoulder" # "肩寬"
    bust = "bust"         # "胸圍"
    waist = "waist"       # "腰圍"
    hip = "hip"           # "臀圍"
    length = "length"     # "衣長"
    sleeve = "sleeve"     # "袖長"
    inseam = "inseam"     # "內檔長"
