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

from telegram import notify

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

        for section in data["data"]:
            products.extend(section["products"])

        if page >= total_pages:
            break

        page += 1

    return products


def get_specs(product):

    specs = {}

    for item in product.get("classification", []):

        specs[item["a"]] = item["b"]

    return specs


def get_price(product):

    try:
        return int(float(product["finalPrice"]))
    except:
        return 99999999


def is_match(product):

    if get_price(product) > MAX_PRICE:
        return False

    specs = get_specs(product)

    processor = specs.get("Processor", "")
    graphics = specs.get("Graphic Card", "")
    memory = specs.get("Memory", "")
    storage = specs.get("Storage", "")
    os = specs.get("Operating System", "")

    if not any(cpu in processor for cpu in CPU):
        return False

    if not any(gpu.lower() in graphics.lower() for gpu in GPU):
        return False

    if "16 GB" not in memory and "32 GB" not in memory and "64 GB" not in memory:
        return False

    if "1 TB" not in storage and "1024 GB" not in storage:
        return False

    if "Windows 11" not in os:
        return False

    return True


def print_product(product):

    specs = get_specs(product)

    print("=" * 70)
    print(product["productName"])
    print(f"₹{get_price(product):,}")
    print(specs.get("Processor", ""))
    print(specs.get("Graphic Card", ""))
    print(specs.get("Memory", ""))
    print(specs.get("Storage", ""))
    print("https://www.lenovo.com" + product["url"])
    print()


def main():

    products = get_all_products()

    print(f"\nTotal products : {len(products)}\n")

    matches = []

    for product in products:

        try:

            if is_match(product):
                matches.append(product)

        except Exception as e:

            print(product.get("productName"))
            print(e)

    print("=" * 70)
    print(f"Matches Found : {len(matches)}")
    print("=" * 70)

    if not matches:
        print("No matching laptops found.")
        return

    for product in matches:
        print_product(product)

    notify(matches)


if __name__ == "__main__":
    main()
