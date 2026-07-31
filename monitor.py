import json
import os
import requests
from bs4 import BeautifulSoup

from config import URL, CPU, GPU, RAM, SSD, MAX_PRICE

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]


def send(msg):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": msg
        }
    )


headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(URL, headers=headers, timeout=30)

print("Status:", response.status_code)

soup = BeautifulSoup(response.text, "lxml")

print("Title:", soup.title.string if soup.title else "No title")

print("Length:", len(response.text))

with open("page.html", "w", encoding="utf-8") as f:
    f.write(response.text)

send("✅ Lenovo Monitor is running successfully.")
