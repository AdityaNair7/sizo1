import json
import urllib.parse
import requests

from config import (
    URL,
    PAGE_FILTER_ID,
    MAX_PRICE,
    CPU,
    GPU,
    RAM,
    SSD,
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/138.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://www.lenovo.com/in/outletin/en/laptops/",
    "Origin": "https://www.lenovo.com",
}


# ----------------------------
# Build API URL
# ----------------------------
def build_url(page):
    payload = {
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
        "subseriesCode": "",
    }

    encoded = urllib.parse.quote(
        json.dumps(payload, separators=(",", ":"))
    )

    return (
        f"{URL}"
        f"?pageFilterId={PAGE_FILTER_ID}"
        f"&params={encoded}"
    )


# ----------------------------
# Download all products
# ----------------------------
def get_all_products():
    products = []

    page = 1

    while True:

        print(f"Downloading page {page}")

        r = requests.get(
            build_url(page),
            headers=HEADERS,
            timeout=30,
        )

        r.raise_for_status()

        data = r.json()["data"]

        if page == 1:
            total_pages = data["pageCount"]

        page_data = data["data"]

        for section in page_data:
            products.extend(section["products"])

        if page >= total_pages:
            break

        page += 1

    return products


# ----------------------------
# Convert classification list
# ----------------------------
def get_specs(product):

    specs = {}

    for item in product.get("classification", []):

        key = item.get("a", "").strip()
        value = item.get("b", "").strip()

        specs[key] = value

    return specs


# ----------------------------
# Safe price conversion
# ----------------------------
def get_price(product):

    raw = product.get("finalPrice", "99999999")

    try:
        return int(float(raw))
    except:
        return 99999999


# ----------------------------
# Filter logic
# ----------------------------
def is_match(product):

    price = get_price(product)

    if price > MAX_PRICE:
        return False

    specs = get_specs(product)

    processor = specs.get("Processor", "")
    graphics = specs.get("Graphic Card", "")
    memory = specs.get("Memory", "")
    storage = specs.get("Storage", "")
    os = specs.get("Operating System", "")

    # CPU
    if not any(cpu in processor for cpu in CPU):
        return False

    # GPU
    if not any(gpu.lower() in graphics.lower() for gpu in GPU):
        return False

    # RAM
    if f"{RAM} GB" not in memory and f"{RAM}GB" not in memory:
        return False

    # SSD
    if f"{SSD} TB" in storage:
        pass
    elif "1 TB" in storage:
        pass
    elif f"{SSD} GB" in storage:
        pass
    elif "1024 GB" in storage:
        pass
    else:
        return False

    # Windows
    if "Windows 11" not in os:
        return False

    return True


# ----------------------------
# Print laptop
# ----------------------------
def print_product(product):

    specs = get_specs(product)

    print("=" * 70)
    print(product["productName"])
    print(f"₹ {get_price(product):,}")
    print(specs.get("Processor", ""))
    print(specs.get("Graphic Card", ""))
    print(specs.get("Memory", ""))
    print(specs.get("Storage", ""))
    print("https://www.lenovo.com" + product["url"])
    print()


# ----------------------------
# Main
# ----------------------------
def main():

    products = get_all_products()

    print()
    print(f"Total products : {len(products)}")
    print()

    matches = []

    for product in products:

        try:
            if is_match(product):
                matches.append(product)
        except Exception as e:
            print(f"Skipped {product.get('productName')} -> {e}")

    print("=" * 70)
    print(f"Matches Found : {len(matches)}")
    print("=" * 70)
    print()

    if not matches:
        print("No matching laptops found.")
        return

    for product in matches:
        print_product(product)


if __name__ == "__main__":
    main()
