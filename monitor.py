import json
import urllib.parse
import requests

from config import *

HEADERS = {
    "User-Agent": "Mozilla/5.0"
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
        "subseriesCode": ""
    }

    encoded = urllib.parse.quote(
        urllib.parse.quote(
            json.dumps(params, separators=(",", ":"))
        )
    )

    r = requests.get(
        URL,
        params={
            "pageFilterId": PAGE_FILTER_ID,
            "subSeriesCode": "",
            "loyalty": "false",
            "params": encoded
        },
        headers=HEADERS,
        timeout=30
    )

    r.raise_for_status()

    return r.json()


# ---------------- Main Program ----------------

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
