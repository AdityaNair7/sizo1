import json
import os
import requests

from config import SENT_FILE

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
CHAT_ID = os.getenv("CHAT_ID", "")


def load_sent():

    if not os.path.exists(SENT_FILE):
        return []

    try:
        with open(SENT_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def save_sent(data):

    with open(SENT_FILE, "w") as f:
        json.dump(data, f, indent=4)


def send_message(text):

    if not BOT_TOKEN or not CHAT_ID:
        print("Telegram credentials not configured.")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "disable_web_page_preview": False,
    }

    r = requests.post(
        url,
        data=payload,
        timeout=30,
    )

    r.raise_for_status()


def notify(products):

    sent = load_sent()

    updated = False

    for product in products:

        product_id = product["productCode"]

        if product_id in sent:
            continue

        sent.append(product_id)
        updated = True

        price = int(float(product["finalPrice"]))

        message = f"""
🔥 Lenovo Outlet Match Found

💻 {product["productName"]}

💰 ₹{price:,}

🔗 https://www.lenovo.com{product["url"]}
"""

        try:
            send_message(message.strip())
            print(f"Telegram sent for {product_id}")
        except Exception as e:
            print(e)

    if updated:
        save_sent(sent)
