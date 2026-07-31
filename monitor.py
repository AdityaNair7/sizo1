import os
import json
import requests

from config import *

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

url = "https://openapi.lenovo.com/in/outletin/en/ofp/search/dlp/product/query/get/_tsc"

params = {
    "pageFilterId": "afdcd3f7-d8e6-4e9e-a76a-d6060dc75ae9",
    "subSeriesCode": "",
    "loyalty": "false",
    "params": json.dumps({
        "classificationGroupIds": "400001",
        "pageFilterId": "afdcd3f7-d8e6-4e9e-a76a-d6060dc75ae9",
        "facets": [],
        "page": "1",
        "pageSize": 30,
        "groupCode": "",
        "init": True,
        "sorts": ["newest", "priceUp"],
        "version": "v2",
        "enablePreselect": True,
        "subseriesCode": ""
    })
}

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, params=params, headers=headers)

print(response.status_code)

with open("response.json", "w", encoding="utf-8") as f:
    f.write(response.text)
