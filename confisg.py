# ==============================
# Lenovo Outlet API
# ==============================

URL = "https://openapi.lenovo.com/in/outletin/en/ofp/search/dlp/product/query/get/_tsc"

PAGE_FILTER_ID = "afdcd3f7-d8e6-4e9e-a76a-d6060dc75ae9"


# ==============================
# Your Filters
# ==============================

MAX_PRICE = 70000


# CPUs you are willing to buy
CPU = [

    # 12th Gen
    "12650HX",
    "12700H",
    "12700HX",
    "12800HX",
    "12900HX",

    # 13th Gen
    "13650HX",
    "13700H",
    "13700HX",
    "13800HX",
    "13900HX",

    # 14th Gen
    "14650HX",
    "14700HX",
    "14900HX",
]


# Minimum GPU accepted
GPU = [

    "RTX 4050",
    "RTX™ 4050",

    "RTX 4060",
    "RTX™ 4060",

    "RTX 4070",
    "RTX™ 4070",

    "RTX 4080",
    "RTX™ 4080",

    "RTX 4090",
    "RTX™ 4090",

    # Future proof
    "RTX 5050",
    "RTX™ 5050",

    "RTX 5060",
    "RTX™ 5060",

    "RTX 5070",
    "RTX™ 5070",

    "RTX 5080",
    "RTX™ 5080",

    "RTX 5090",
    "RTX™ 5090",
]


# Minimum RAM
RAM = 16


# Minimum SSD (GB)
SSD = 1024


# Windows required
REQUIRE_WINDOWS = True


# ==============================
# Telegram
# (Fill these later)
# ==============================

BOT_TOKEN = ""

CHAT_ID = ""


# ==============================
# Duplicate protection
# ==============================

SENT_FILE = "sent.json"
