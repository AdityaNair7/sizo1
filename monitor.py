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

    # Convert JSON to compact string
    json_string = json.dumps(params, separators=(",", ":"))

    # Double encode exactly like Lenovo
    encoded = urllib.parse.quote(
        urllib.parse.quote(json_string, safe=""),
        safe=""
    )

    # Build URL manually (don't let requests encode again)
    url = (
        f"{URL}"
        f"?pageFilterId={PAGE_FILTER_ID}"
        f"&subSeriesCode="
        f"&loyalty=false"
        f"&params={encoded}"
    )

    print(url)  # Remove later after debugging

    r = requests.get(
        url,
        headers=HEADERS,
        timeout=30,
    )

    print("Status Code:", r.status_code)

    r.raise_for_status()

    return r.json()


# ---------------- Main Program ----------------

products = []

page = 1

while True:

    print(f"\nDownloading page {page}")

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
