import json
import urllib.parse
import requests

from config import *

HEADERS = {
    "Accept": "*/*",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://www.lenovo.com",
    "Referer": "https://www.lenovo.com/",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36",
}


def get_page(page):
    params = {
        "classificationGroupIds": "400001",
        "pageFilterId": PAGE_FILTER_ID,
        "facets": [],
        "page": page,
        "pageSize": 30,
        "groupCode": "",
        "init": True,
        "sorts": ["newest", "priceUp"],
        "version": "v2",
        "enablePreselect": True,
        "productIndex": "",
        "subseriesCode": ""
    }

    json_string = json.dumps(params, separators=(",", ":"))

    encoded = urllib.parse.quote(
        urllib.parse.quote(json_string, safe=""),
        safe=""
    )

    url = (
        f"{URL}"
        f"?pageFilterId={PAGE_FILTER_ID}"
        f"&subSeriesCode="
        f"&loyalty=false"
        f"&params={encoded}"
    )

    r = requests.get(
        url,
        headers=HEADERS,
        timeout=30,
    )

    r.raise_for_status()

    return r.json()


def get_specs(product):
    specs = {}

    for item in product.get("classification", []):
        specs[item["a"]] = item["b"]

    return specs


def is_match(product):
    specs = get_specs(product)

    price = product.get("finalPrice", 99999999)

    cpu = specs.get("Processor", "")
    gpu = specs.get("Graphic Card", "")
    ram = specs.get("Memory", "")
    storage = specs.get("Storage", "")

    if price > MAX_PRICE:
        return False

    if not any(x in cpu for x in CPU):
        return False

    if not any(x in gpu for x in GPU):
        return False

    if f"{RAM} GB" not in ram:
        return False

    if "1 TB" not in storage:
        return False

    return True


# ==========================
# Main Program
# ==========================

products = []

page = 1

while True:

    print(f"Downloading page {page}")

    data = get_page(page)

    pages = data["data"]["pageCount"]
    groups = data["data"]["data"]

    if not groups:
        break

    for group in groups:
        products.extend(group["products"])

    if page >= pages:
        break

    page += 1


print(f"\nTotal products: {len(products)}")

matches = []

for product in products:
    if is_match(product):
        matches.append(product)

print(f"Matching laptops: {len(matches)}\n")

for product in matches:

    specs = get_specs(product)

    print("=" * 70)
    print(product["productName"])
    print(f"Price      : ₹{product['finalPrice']}")
    print(f"Processor  : {specs.get('Processor', '-')}")
    print(f"Graphics   : {specs.get('Graphic Card', '-')}")
    print(f"Memory     : {specs.get('Memory', '-')}")
    print(f"Storage    : {specs.get('Storage', '-')}")
    print(f"Condition  : {product.get('productCondition', '-')}")
    print(f"Product ID : {product['productCode']}")
    print(f"URL        : {product['url']}")
    print()
